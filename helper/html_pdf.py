# from weasyprint import HTML, CSS
# from weasyprint.text.fonts import FontConfiguration

# def template_one_html(json_resume):
#     #parse json code
    
    
    
    
#     username = ""
    
    
    
#     #create section in html using informations
    
    
    
#     # apply css style
#     css_code = ""
    
    
#     #concat all section to get html code
    
    
#     html_code = ""
    
#     return html_code, css_code, username

# def html_to_pdf(json_resume):
#     html_code, css_code, username = template_one_html(json_resume)
#     font_config = FontConfiguration()
#     html = HTML(string=html_code) # html_code should return html code in a string
#     css = CSS(string=css_code, font_config=font_config) # css_code should return css code in a string
#     html.write_pdf(f'{username}.pdf', stylesheets=[css], font_config=font_config) # username should be retrieved from the json file