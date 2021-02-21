from mesa.visualization.modules import TextElement

class Label(TextElement):

    def __init__(self, label, content = None, font = 21, content_font = 18):
        self.label          = label
        self.font           = font
        self.content        = content
        self.content_font   = content_font

    def render(self, model):
        render_html = "<br/>  <div style = 'font-size: " + str(self.font) + "px;'>" + self.label + "</div>" 

        if self.content != None:
        
            render_html += "<div class = 'col-lg-6 col-md-6 col-sm-6 col-xs-6' style = 'font-size: "  + str(self.content_font) + "px; margin-bottom: 10px;'>" 
            render_html += "<br/> Susceptible Agents: "      + str(self.content["Susceptible"](model))
            render_html += "<br/> Exposed Agents: "          + str(self.content["Exposed"](model))
            render_html += "<br/> Infected Agents: "         + str(self.content["Infected"](model))
            render_html += "</div>"
            render_html += "<div class = 'col-lg-6 col-md-6 col-sm-6 col-xs-6' style = 'font-size: "  + str(self.content_font) + "px; margin-bottom: 10px;'>" 
            render_html += "<br/> Died Agents: "             + str(self.content["Deaths"](model))
            render_html += "<br/> Recovered Agents: "        + str(self.content["Recovered"](model))
            render_html += "<br/> Vaccinated Agents: "       + str(self.content["Vaccinated"](model))
            render_html += "</div> <br/>"
                        
        return render_html