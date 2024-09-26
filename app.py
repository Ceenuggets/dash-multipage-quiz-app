import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],
                use_pages=True)

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col([

            html.Div([
                html.Div([dbc.NavLink(f"{page['name']} ", href=page["relative_path"],
                                      active="exact",
                                      className="nav-link",
                                      )],
                         className="me-5 link-div ",
                         ) for page in dash.page_registry.values()
            ], className="d-flex flex-row justify-content-center nav-bar-div",
            ),

            dash.page_container
        ], xs=12, sm=12, md=8, lg=6, xl=6),
    ], justify="center", className='g-0'),
    print(dash.page_registry.values())
], className="index", fluid=True);

if __name__ == '__main__':
    app.run(debug=True)
