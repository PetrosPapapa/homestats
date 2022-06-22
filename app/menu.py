import dash
from dash import html, dcc

layout = html.Nav([
    html.Ul([
        dcc.Link(
            html.Li(
                f"{page['name']}" # - {page['path']}"
            ), href=page["relative_path"]
        )
        for page in dash.page_registry.values()
    ])
])
    
