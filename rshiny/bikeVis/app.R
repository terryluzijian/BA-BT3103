library(shiny)
library(leaflet)
library(httr)
library(jsonlite)
library(geosphere)

building <- fromJSON("data/building.json")

ui <- fluidPage(
  titlePanel("BIKE Avaibility"),
  sidebarLayout(
    sidebarPanel(
      radioButtons("radio", "Type of bike", choices=c("obike","mobike","both"), selected="both"),
      selectInput("select", "Find the nearest bike from", choices=building$name),
      sliderInput("slider", "Whithin the range of (meters)", min = 0, max = 1000, value = 300)
    ),
    mainPanel(
      img(src="obikelabel.png", height = 20),
      img(src="mobikelabel.png", height = 20),
      leafletOutput("map"),
      tableOutput("table")
    )
  )
)


server <- function(input, output) {
  
  #data
  obikeinfo <- fromJSON("https://mobile.o.bike/api/v1/bike/list?latitude=1.2966&longitude=103.7764")
  obikeloc <- obikeinfo$data$list
  obikeloc$imei <- obikeloc$iconUrl <- obikeloc$promotionActivityType <- obikeloc$rideMinutes <- obikeloc$countryId <- obikeloc$helmet <- NULL
  obikeloc$bike <- "obike"
  mobikeinfo <- fromJSON("https://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do?latitude=1.2966&longitude=103.7764")
  mobikeloc <- mobikeinfo$object
  mobikeloc$distNum <- mobikeloc$distance <- mobikeloc$bikeIds <- mobikeloc$biketype <- mobikeloc$type <- mobikeloc$boundary <- NULL
  colnames(mobikeloc) <- c("id","longitude","latitude")
  mobikeloc$bike <- "mobike"
  bikeloc <- rbind(obikeloc, mobikeloc)

  displaybikeloc <- reactive({
    for (n in 1:nrow(bikeloc)){
      long1 <- bikeloc$longitude[n]
      lat1 <- bikeloc$latitude[n]
      long2 <- building[building$name==input$select,]$lon[1]
      lat2 <- building[building$name==input$select,]$lat[1]
      bikeloc$distance[n] <- distGeo(c(long1,lat1),c(long2,lat2))
    }
    temp1 <- bikeloc[, c("id","bike","distance")][bikeloc$distance<input$slider,]
    temp <- temp1[order(temp1$distance),]
    if (input$radio == "obike")
      return(temp[temp$bike=="obike",])
    else if (input$radio == "mobike")
      return(temp[temp$bike=="mobike",])
    else if (input$radio == "both")
      return(temp)
  })
  
 output$table <- renderTable({
    displaybikeloc()
  }, hover=TRUE)
 
 filteredbikeloc <- reactive({
   if (input$radio == "obike")
     bikeloc[bikeloc$bike=="obike",]
   else if (input$radio == "mobike")
     bikeloc[bikeloc$bike=="mobike",]
   else if (input$radio == "both")
     bikeloc
 })
  
  output$map <- renderLeaflet({
    leaflet(data)%>%
      addTiles() %>%
      fitBounds(lng1=103.764489, lat1=1.286334, lng2=103.787914, lat2=1.311692)
  })
  
  observe({
    leafletProxy("map", data=filteredbikeloc()) %>%
      clearMarkers() %>%
      addMarkers(~longitude, ~latitude, label = ~id, 
        icon=icons(iconUrl=ifelse(filteredbikeloc()$bike=="obike","obikemarker.png","mobikemarker.png"), iconWidth = 50, iconHeight = 50, iconAnchorX = 25, iconAnchorY = 50)
        ) %>%
      clearShapes() %>%
      addCircleMarkers(data=building[building$name==input$select,], ~lon, ~lat, stroke = FALSE, fillOpacity = 0.5) %>%
      addCircles(data=building[building$name==input$select,], ~lon, ~lat, weight=0, radius=input$slider)
  })
}

shinyApp(ui, server)