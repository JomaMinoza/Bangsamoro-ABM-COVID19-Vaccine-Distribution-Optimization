from mesa.visualization.modules import ChartModule, TextElement

class SummaryChartModule(ChartModule):
    default_series = [
                {"Label": "Susceptible","Color": "Brown"},
                {"Label": "Exposed","Color": "Orange"},
                {"Label": "Infected","Color": "Red"},
                {"Label": "Recovered","Color": "Green"},
                {"Label": "Deaths","Color": "Black"},
                {"Label": "Vaccinated","Color": "Yellow"}
    ]
    def __init__(self, 
                 canvas_width, 
                 canvas_height, 
                 data_collector = "datacollector", 
                 series = default_series, 
                 geospatial = False, 
                 location_index = 0
                ):
        super().__init__(
            series              = series,
            canvas_width        = canvas_width,
            canvas_height       = canvas_height,
            data_collector_name = data_collector,
            geospatial          = geospatial,
            location_index      = location_index
        )