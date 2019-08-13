setwd("~/Documents/GitHub/LEADS-Publisher-Names/leads-2019")
library(igraph)

clean_df = function(community, a) {
  if (a == 1) {
    len = 3789
  } else {
    len = 3679
  }
  colnames(community) = c("node", "group")
  community$node = community$node - 1
  community_pub = community[community$node <= len,]
  return(community_pub)
}

# x being the algorithm  
# y being whether weighted or not
# z being whether considering the relationship between publishers or not "Y" or "N"
filename = function(a, x, y, z) {
  if (a == 1) {
    string_3 = "pre"
  } else {
    string_3 = "npre"
  }
  if (z == "Y") {
    string2 = "imp"
  } else {
    string2 = "nimp"
  }
  if (y == "unweighted") {
    string1 = "unweighted"
  } else {
    string1 = "weighted"
  }
  
  filename = paste("./processed_data_10k_cluster/", x, "-", string_3, "-",
                   string1, "-", string2, ".csv", sep = "")
  return(filename)
}

clustering = function(a, x, y, z) {
  
  if (a == 1) {
    data = read.csv("./processed_data_10k/cluster_result_1.csv",
                    stringsAsFactors = F)
  } else {
    data = read.csv("./processed_data_10k/cluster_result_2.csv",
                    stringsAsFactors = F)
  }
  
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
  
  network_file1 = read.csv("./processed_data_10k/isbn_df.csv", stringsAsFactors = F)
  if (z == "Y") {
    network_file1 = network_file1[, c(1:3)]
  } else {
    network_file1 = network_file1[network_file1$type == 1,]
    network_file1 = network_file1[, c(1:3)]
  }
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
  
  write.csv2(as.numeric(mod), file = filename(a, x, y, z))
  data = read.csv(filename(a, x, y, z), stringsAsFactors = F, sep = ";")
  data = clean_df(data, a)
  
  return(data)
}

files = list.files("./processed_data_10k_cluster/")
raw = read.csv("./processed_data_10k/publisher_10k_p1.csv", stringsAsFactors = F)
cluster1 = read.csv("./processed_data_10k/cluster_result_1.csv", stringsAsFactors = F)
cluster2 = read.csv("./processed_data_10k/cluster_result_2.csv", stringsAsFactors = F)
cluster = merge(
  x = cluster1[, c(1, 3)], y = cluster2[, c(1, 3)],
  by = "text",
  all = T
)

for (i in 1:3) {
  x = c("walktrap", "louvain", "infomap")[i]
  for (j in 1) {
    y = c("unweighted")[j]
    for (z in c("N", "Y")) {
      for (a in 1:2) {
        print(filename(a, x, y, z))
        data = clustering(a, x, y, z)
        colnames(data)[2] = strsplit(filename(a, x, y, z), ".csv")[[1]][1]
        
        if (a == 1) {
          cluster1 = merge(
            x = cluster1, y = data,
            by.x = "id", by.y = "node",
            all = T
          )
        } else {
          cluster2 = merge(
            x = cluster2, y = data,
            by.x = "id", by.y = "node",
            all = T
          )
        }
        
      }
    }
  }
}

write.csv(cluster, "./processed_data_10k/grouped_cluster_10k_final.csv", row.names = F)
write.csv(cluster1, "cluster_result1.csv", row.names = F)
write.csv(cluster2, "cluster_result2.csv", row.names = F)

