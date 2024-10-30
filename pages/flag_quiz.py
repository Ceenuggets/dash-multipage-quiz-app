import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import random
from .data import countries



sample = list(countries.keys())

"======================= Generate countries Randomly ==========="


def select_random_countries():
    select_countries = []
    n = 0
    while n < 10:
        country = random.choice(sample)
        if country not in select_countries:
            select_countries.append(country)
            # print(f"{n}. {country}")
            n += 1
    # print(select_countries)
    return select_countries
"================================================================"


"======== Generate 3 random wrong answers ============="


def provide_random_answers(answer):
    m = 0
    country_options = []
    country_options.append(answer)
    while m < 3:
        incorrect_option = random.choice(sample)
        if (incorrect_option.strip().lower() != answer.strip().lower()) and (incorrect_option not in country_options):
            country_options.append(incorrect_option)
            m += 1
    random.shuffle(country_options)
    return country_options
"==================================================="

dash.register_page(__name__, name="Flag Quiz", path="/")

layout = dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div("Country Flag Identification", id="title"),
                        html.Div(id="report"),
                        html.Div(id="test_result"),
                    ], id="result_display"),
                    html.Div([
                        html.Div([
                            html.P(id="steps"),
                            html.Img(id="flag")
                        ], id="flag_div"),
                        html.Div([
                            dcc.RadioItems(id="rd_countries")
                        ], id="answer_options"),
                    ], id="flag_question_display"),
                    html.Div([
                        html.Div(id="all_correct_answers"),
                    ], id="summary_display")
                ], id="parent_div")
            ], xs=12, sm=12, md=12, lg=12, xl=12),
            dcc.Store(id="select_countries_store", data=None),
            dcc.Store(id="correct_answer", data=None),
            dcc.Store(id="result", data={}),
            dcc.Store(id="num_answered", data=0),
            dcc.Store(id="all_correct_answers_store", data=[]),
            # dcc.Store(id="store_result_data",),
        ], justify="center", className="g-0 fq"),


@callback(
    Output("report", "children"),
    Output("steps", "children", allow_duplicate=True),
    Output("flag", "src"),
    Output("rd_countries", "options"),
    Output("correct_answer", "data"),
    Output("select_countries_store", "data", allow_duplicate=True),
    Output("num_answered", "data"),
    Output("result", "data"),
    [Input("select_countries_store", "data")],
    [State("result", "data"),
     State("num_answered", "data")],
    prevent_initial_call=True
)
def display_country_info(country_names, result, num_answered):
    # global num_answered
    # global result
    random_ten = select_random_countries()
    if not country_names:
        options = [{"label": option, "value": option} for option in provide_random_answers(random_ten[0])]
        num_answered += 1

        report = [html.Span("✅" if val == "pass" else "❌",
                            style={'margin-right': '1px', 'font-size': '20px',
                                   'font-weight': 'bold', 'color': 'forestgreen' if val == "pass" else 'red'})
                  for val in result.values()]
        if len(random_ten) == 10:
            result = {}
        # print(report)
        # print(random_ten)
        # print((10 - (len(random_ten))) + 1)
        return report, f"{(10 - (len(random_ten))) + 1} of 10", f"/assets/flags/{random_ten[0]}.jpg", options, \
        random_ten[0], random_ten, num_answered, result
    else:

        options = [{"label": option, "value": option} for option in provide_random_answers(country_names[0])]
        if len(country_names) == 10:
            result = {}

        # print(country_names)
        # report = [html.Span("—", style={'margin-right': '10px', 'font-size': '24px', 'font-weight': 'bold',
        #                                 'color': 'forestgreen' if key == "pass" else 'red'})
        #           for key in result.values()]

        report = [html.Span("✅" if val == "pass" else "❌",
                            style={'margin-right': '1px', 'font-size': '20px',
                                   'font-weight': 'bold', 'color': 'forestgreen' if val == "pass" else 'red'})
                  for val in result.values()]

        # print(report)
        # print((10 - (len(country_names)) + 1))
        return report, f"{(10 - (len(country_names)) + 1)} of 10", f"/assets/flags/{country_names[0]}.jpg", options, \
        country_names[0], country_names, num_answered, result



@callback(
    Output("test_result", "children"),
    Output("steps", "children", allow_duplicate=True),
    Output("rd_countries", "options", allow_duplicate=True),
    Output("select_countries_store", "data", allow_duplicate=True),
    Output("all_correct_answers", "children"),
    Output("num_answered", "data", allow_duplicate=True),
    Output("result", "data", allow_duplicate=True),
    Output("all_correct_answers_store", "data"),
    [Input("rd_countries", "value")],
    [State("correct_answer", "data"),
     State("rd_countries", "options"),
     State("select_countries_store", "data"),
     State("num_answered", "data"),
     State("result", "data"),
     State("all_correct_answers_store", "data")],
    prevent_initial_call=True
)
def select_answer(select_answer, correct_answer, options, chosen_countries, num_answered, result, all_correct_answers_store):
    # global num_answered
    # global result
    # global all_correct_answers
    print(result)
    number_passed = 0
    for country in chosen_countries:
        updated_options = []
        # print(chosen_countries)
        # print(options)
        if select_answer and correct_answer:
            for option in options:
                label = option["label"]
                key = str((10 - (len(chosen_countries))) + 1)

                if label != correct_answer and label == select_answer:
                    label += " ❌ "
                    if key not in result.keys():
                        result[key] = "fail"
                        # print(key)
                        # print(result)

                elif label == correct_answer and label == select_answer:
                    label += " ✅ "
                    # key = ((10 - (len(chosen_countries))) + 1)
                    if key not in result.keys():
                        result[key] = "pass"
                        # print(key)
                        # print(result)

                    chosen_countries.remove(correct_answer)
                    all_correct_answers_store.append(correct_answer)

                    for value in result.values():
                        if value == "pass":
                            number_passed += 1
                    if len(result.values()) == 10:
                        img_results = [
                            html.Div([html.Div([
                                html.Img(src=f"/assets/flags/{country}.jpg",
                                         style={'width': '80px', 'height': '60px'}),
                                html.P(country,
                                       style={'text-align': 'left', 'margin-top': '0px', 'margin-bottom': '0px',
                                              'color': 'white'}),
                            ], className="country_flags_results"),
                            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
                                      'margin-top': '5px'}) for country in all_correct_answers_store]

                        all_correct_answers_store = []
                        return f"Result: {number_passed}/10", f"{num_answered} of 10", updated_options, chosen_countries, img_results, num_answered, result, all_correct_answers_store
                    else:
                        return f"Result: {number_passed}/10", f"{num_answered} of 10", updated_options, chosen_countries, [], num_answered, result, all_correct_answers_store
                else:
                    label = option["label"]
                updated_options.append({'label': label, 'value': option['value']})
        for value in result.values():
            if value == "pass":
                number_passed += 1
        return f"Result: {number_passed}/10", f"{(10 - (len(chosen_countries)) + 1)} of 10", updated_options, dash.no_update, [], num_answered, result, all_correct_answers_store

