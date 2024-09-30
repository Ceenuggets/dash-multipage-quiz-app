import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import random
from .data import countries
from .countries_data import countries_info


sample = list(countries.keys())
capitals = list(countries.values())


"======== Generate country and options ============="
def question_and_options():
    m = 0
    options =[]
    question = random.choice(sample)
    answer = countries[question]
    options.append(answer)
    while m < 3:
        incorrect_option = random.choice(capitals)
        if (incorrect_option.strip().lower() != answer.strip().lower()) and (incorrect_option not in options):
            options.append(incorrect_option)
            m += 1
    random.shuffle(options)
    return question, options, answer

"==================================================="


dash.register_page(__name__, name="Country Quiz", path="/country_info")

# print(countries_info)
layout = dbc.Row([
    dbc.Col([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H5(id="question"),
                        html.Button("Next", id="btn_next")
                    ], id="question_div"),
                    html.Div([
                        dcc.RadioItems(id="rd_capitals")
                    ], id="options_div"),
                ], id="question_options_div"),
                html.Div([
                        html.Div([

                    ], id="country_table"),
                    html.Div([
                        html.Div([
                             html.Img(id="country_img")
                        ], id="flag_img_div"),
                        html.Div([

                            ], id="indpndnc_date")
                    ], id="country_more_info")
                ], id="country_table_and_flag"),
                html.Div([
                 
                ], id="city_div")
            ])
        ], id="div_parent")
    ], xs=12, sm=12, md=12, lg=12, xl=12),
    dcc.Store(id="right_answer", data=None),
], justify="center", className="g-0 ci")


@callback(
    Output("question", "children"),
    Output("rd_capitals", "options"),
    Output("right_answer", "data"),
    [Input("btn_next", "n_clicks")]
)
def display_question(n_clicks):
    if n_clicks:
        question, choices, right_answer = question_and_options()
        options = [{"label": choice, "value": choice}for choice in choices]
        country_and_capital = {"Country": question, "Capital": right_answer}
        return question, options, country_and_capital
    else: 
        question, choices, right_answer = question_and_options()
        options = [{"label": choice, "value": choice}for choice in choices]
        country_and_capital = {"Country": question, "Capital": right_answer}
        return question, options, country_and_capital


@callback(
    Output("rd_capitals", "options", allow_duplicate=True),
    Output("country_table", "children"),
    Output("country_img", "src"),
    Output("country_img", "style"),
    Output("indpndnc_date", "children"),
    Output("city_div", "children"),
    [Input("rd_capitals", "value"),
     State("rd_capitals", "options"),
     State("right_answer", "data")],
    prevent_initial_call=True
)
def check_answers(select_capital, options, solution):
    if select_capital and solution:
        table_body = []
        table_div = ""
        govt_type = ""
        date_of_independence = ""
        pop_cities = ""
        updated_options = []
        for option in options:
            label = option["label"]
            if label != solution["Capital"] and label == select_capital:
                label += " ❌ "
                flag_src = ""
            elif label == solution["Capital"] and label == select_capital:
                label += " ✅ "
                right_answer_details = countries_info[solution["Country"]]
                table_rows = [html.Tr([html.Td("Continent:"), html.Td(right_answer_details["Continent"])]),
                                html.Tr([html.Td("Capital:"), html.Td(solution["Capital"])]),
                                html.Tr([html.Td("Languages:"), html.Td(', '.join(right_answer_details["Languages"]))]),
                                html.Tr([html.Td("Currency:"), html.Td(right_answer_details["Currency"])]),
                                html.Tr([html.Td("Time Zones:"), html.Td(', '.join(right_answer_details["TimeZones"]))]),
                                html.Tr([html.Td("GMT Offset:"), html.Td(', '.join(right_answer_details["GMTOffSets"]))]),
                                html.Tr([html.Td("Govt. Type:"), html.Td(', '.join(right_answer_details["GovernmentTypes"]).capitalize())]),
                                html.Tr([html.Td("Motto:"), html.Td(right_answer_details["Motto"])]),
                              ]
                for row in table_rows:
                    table_body.append(row)
                table_div = html.Div([
                    html.Table([
                        html.Tbody(table_body)
                    ])
                ])
                flag_src = f"/assets/flags/{solution["Country"]}.jpg"
                govt_type = html.Ul([html.Li(item.capitalize()) for item in right_answer_details["GovernmentTypes"]])
                

                indpndce_date= right_answer_details["IndependenceDate"]

                date_of_independence = html.Div([
                    html.Div("Independence", id="indp_div"),
                    html.Div(indpndce_date, id="indp_date"),
                ], className="img_date_container")


                cities = right_answer_details["Cities"]
                pop_cities = [ html.Div(city, className="pop_city") for city in cities]
                print(pop_cities)
            updated_options.append({'label': label, 'value': option['value']}) 
        return updated_options, table_div, flag_src, {"width": "200px", "height": "auto" }, date_of_independence,pop_cities
    else:
        return dash.no_update, dash.no_update, dash.no_update,{"width": "0", "height": "0"}, date_of_independence, pop_cities