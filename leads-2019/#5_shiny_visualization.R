library(networkD3)

data = read.csv("./processed_data_1m/cluster_result_final.csv",
                stringsAsFactors = F)
data = data[is.na(data$..processed_data_1m.infomap.unweighted) == F,]

# x is the number of cluster of infomap
cluster_visualization = function(x) {
  
  data = data[data$..processed_data_1m.infomap.unweighted == x, c(4, 5)]
  edge = data.frame()
  
  for (i in 1:nrow(data)) {
    publisher = data$publisher[i]
    isbns = strsplit(data$isbn[i], ";")[[1]]
    
    edge = rbind(
      edge,
      data.frame(source = publisher,
                 target = isbns,
                 stringsAsFactors = F)
    )
  }
  
  node1 = data.frame(unique(data.frame(edge$source)))
  node2 = data.frame(unique(data.frame(edge$target)))
  colnames(node1) = colnames(node2) = "nName"
  node = rbind(node1, node2)
  node$ID = 1:nrow(node)
  
  data_1 = merge(edge, node,
                 by.x = "source", by.y = "nName", 
                 all.x = T)
  data_1 = merge(data_1, node,
                 by.x = "target", by.y = "nName", 
                 all.x = T)
  colnames(data_1)[c(3, 4)] = c("sourceID", "targetID")
  rownames(data_1) = 0:(nrow(data_1) - 1)
  edge = data_1
  edge$sourceID = edge$sourceID - 1
  edge$targetID = edge$targetID - 1
  node$group[node$nName %in% edge$source] <- "source"
  node$group[node$nName %in% edge$target] <- "target"
  
  D3_network_LM <- forceNetwork(Links = edge, Nodes = node, Source = "sourceID", 
                                Target = "targetID", NodeID = "nName", Group = "group",
                                height = 500, width = 1000, fontSize = 20, 
                                opacity = 0.85, zoom = TRUE)
  return(D3_network_LM)
}

network = cluster_visualization(9)
network


