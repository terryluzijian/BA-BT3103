library(shiny)
library(leaflet)
library(httr)
library(jsonlite)

ui <- fluidPage(
  titlePanel("Realtime Taxi Avaibility Visualisation"),
  leafletOutput("taxi"),
  actionButton("update", "Update"),
  helpText("Last Updated:", textOutput("currentTime"))
)
  

server <- function(input, output) {
  
  output$currentTime <- renderText({
    input$update
    format(Sys.time())
  })
  
  output$taxi <- renderLeaflet({
    input$update
    url <- "http://datamall2.mytransport.sg/ltaodataservice"
    resp <- GET(paste0(url, 
                       "/Taxi-Availability"), 
                add_headers(AccountKey = "RRRqDS+yQ4uUhETHF+Clvg==",
                            accept = "application/json"))
    taxiinfo <- fromJSON(content(resp, "text"), 
                         simplifyDataFrame = TRUE)
    taxilocation <- taxiinfo$value
    
    leaflet(data = taxilocation)%>%
      addTiles() %>%
      addMarkers(~Longitude,~Latitude) %>%
      fitBounds(lng1=103.764489, lat1=1.286334, lng2=103.787914, lat2=1.311692)
  })
}

shinyApp(ui, server)