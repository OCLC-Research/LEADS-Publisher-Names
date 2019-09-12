setwd("~/Documents/GitHub/LEADS-Publisher-Names/leads-2019")
library(igraph)

# x being the algorithm  
# y being whether weighted or not
filename = function(x, y) {
  if (y == "unweighted") {
    string1 = "unweighted"
  } else {
    string1 = "weighted"
  }
  
  filename = paste("./processed_data_1m/", x, "-", string1, ".csv", sep = "")
  return(filename)
}

clustering = function(x, y) {
  
  data = read.csv("./processed_data_1m/cluster_result_single.csv",
                    stringsAsFactors = F)

  network_file = data.frame()
  
  for (i in 1:nrow(data)) {
    id = data$id[i]
    isbns = strsplit(data$isbn_new[i], ";")[[1]]
    
    network_file = rbind(
      network_file,
      data.frame(
        id = id,
        isbn = isbns,
        stringsAsFactors = F
      )
    )
  }
  
  network_file1 = read.csv("./processed_data_1m/isbn_df_simple.csv", stringsAsFactors = F)
  network_file1 = network_file1[network_file1$type == 1,]
  network_file1 = network_file1[, c(1:3)]
  
  colnames(network_file1) = c("id", "isbn", "weight")
  network_file2 = merge(
    network_file, network_file1,
    by.x = c("id", "isbn"),
    by.y = c("id", "isbn")
  )
  
  if (y == "unweighted") {
    
    g <- graph.data.frame(network_file, directed=FALSE)
    bipartite.mapping(g)
    V(g)$type <- bipartite_mapping(g)$type
    
    if (x == "walktrap") {
      wc = cluster_walktrap(g)
      mod = membership(wc)
    } else if (x == "louvain") {
      wc = cluster_louvain(g)
      mod = membership(wc)
    } else if (x == "infomap") {
      wc = cluster_infomap(g)
      mod = membership(wc)
    }
    
  } else {
    g <- graph.data.frame(network_file2, directed=FALSE)
    bipartite.mapping(g)
    V(g)$type <- bipartite_mapping(g)$type
    
    if (x == "walktrap") {
      wc = cluster_walktrap(g)
      mod = membership(wc)
    } else if (x == "louvain") {
      wc = cluster_louvain(g)
      mod = membership(wc)
    } else if (x == "infomap") {
      wc = cluster_infomap(g, e.weights = network_file2$weight)
      mod = membership(wc)
    }
  }
  
  write.csv2(as.numeric(mod), file = filename(x, y))
  data = read.csv(filename(x, y), stringsAsFactors = F, sep = ";")
  
  return(data)
}

cluster1 = read.csv("./processed_data_1m/cluster_result_single.csv", stringsAsFactors = F)

network_file1 = read.csv("./processed_data_1m/isbn_df_simple.csv", stringsAsFactors = F)
network_file1 = network_file1[network_file1$type == 1,]
network_file1 = network_file1[, c(1:3)]

for (i in 1:3) {
  x = c("walktrap", "louvain", "infomap")[i]
  for (j in 1) {
    y = c("unweighted")[j]
    print(filename(x, y))
    data = clustering(x, y)
    data = data[1:max(network_file1$cluster_id),]
    colnames(data)[1] = "node"
    colnames(data)[2] = strsplit(filename(x, y), ".csv")[[1]][1]
    data$node = data$node - 1
    
    cluster1 = merge(
      x = cluster1, y = data,
      by.x = "id", by.y = "node",
      all = T
    )
  }
}

write.csv(cluster1, "./processed_data_1m/cluster_result_final.csv", row.names = F)

