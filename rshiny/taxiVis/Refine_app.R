library(shiny)
library(leaflet)
library(httr)
library(jsonlite)

ui <- fluidPage(
  tags$link(rel = 'stylesheet', type = 'text/css', href = 'bootstrap.css'),
#  titlePanel("TAXI Avaibility"),
  leafletOutput("map", width = '100%'),
  actionButton("update", "Update"),
  h5("Auto update every one minute"),
  h6("Last Updated:", textOutput("currentTime"))
)


server <- function(input, output) {

  output$currentTime <- renderText({
    input$update
    invalidateLater(60000)
    format(Sys.time())
  })

  output$map <- renderLeaflet({
    leaflet(data)%>%
      addTiles(urlTemplate = 'https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoic2hlbmd5dTk3MDUiLCJhIjoiY2o5c2x0ZGIxMHN4OTJ3cXFpcHFuMXB3diJ9.D65rkuZ55BxhUqyl2c0SZg',
               attribution = 'Maps by <a href="http://www.mapbox.com/">Mapbox</a>') %>%
      fitBounds(lng1=103.764489, lat1=1.286334, lng2=103.787914, lat2=1.311692)
  })

  observe({
    input$update
    invalidateLater(60000)
    url <- "http://datamall2.mytransport.sg/ltaodataservice"
    resp <- GET(paste0(url,
                       "/Taxi-Availability"),
                add_headers(AccountKey = "RRRqDS+yQ4uUhETHF+Clvg==",
                            accept = "application/json"))
    taxiinfo <- fromJSON(content(resp, "text"),
                         simplifyDataFrame = TRUE)
    taxilocation <- taxiinfo$value
    leafletProxy("map", data=taxilocation) %>%
      clearMarkers() %>%
      addMarkers(~Longitude,~Latitude)
  })
}

shinyApp(ui, server)
