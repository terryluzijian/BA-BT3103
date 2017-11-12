library(shiny)
library(leaflet)
library(httr)
library(jsonlite)

ui <- fluidPage(
  titlePanel("TAXI Avaibility"),
  leafletOutput("map"),
  h6("Auto update every one minute"),
  actionButton("update", "Update"),
  helpText("Last Updated:", textOutput("currentTime"))
)
  

server <- function(input, output) {
  
  output$currentTime <- renderText({
    input$update
    invalidateLater(60000)
    format(Sys.time())
  })
  
  output$map <- renderLeaflet({
    leaflet(data)%>%
      addTiles() %>%
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