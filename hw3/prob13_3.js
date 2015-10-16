
function kMeansClustering(clusters,distFunc){
    var data = clustersToData(clusters);
    var retVal = "";
    var clusterMeans = centroidUpdate(clusters);
    retVal += "Original clusters "+clusteringToString(clusters)+" have means "+ clusteringToString(clusterMeans)+ "</br>";
    
    var newClusters = clusterAssignment(data,clusterMeans,distFunc);
    clusterMeans = centroidUpdate(newClusters);
    var iteration = 1;
    retVal += "Iteration 1 has clusters "+clusteringToString(newClusters)+" with means "+ clusteringToString(clusterMeans)+ "</br>";
    while( !dataClusteringsAreEqual(clusters,newClusters)){
        clusters = newClusters;
        clusterMeans = centroidUpdate(clusters);
        newClusters = clusterAssignment(data,clusterMeans,distFunc);
        iteration++;
        retVal += "Iteration "+iteration+" has clusters "+clusteringToString(newClusters)+" with means "+clusteringToString(clusterMeans) + "</br>";
    }
    
    return retVal;
}

function dataClusteringsAreEqual(c1,c2){
    if(c1.length != c2.length){return false;}
    
    for(var clusterIndex=0;clusterIndex<c1.length;clusterIndex++){
        if(c1[clusterIndex].length != c2[clusterIndex].length){return false;}
        else{
            for(var dataPtIndex=0;dataPtIndex<c1[clusterIndex].length;dataPtIndex++){
                if(! dataPointsAreEqual(c1[clusterIndex][dataPtIndex],c2[clusterIndex][dataPtIndex])){
                    return false;
                }
            }
        }
    }
    return true;
}

function clustersToData(clustersList){
    var data = []
    clustersList.forEach(function(cluster){
        data = data.concat(cluster);
    });
    return data;
}

function clusterAssignment(data,clusterMeans,distFunc){
    var clusters = [];
    //make clusters array the same size as clusterMeans array
    clusterMeans.forEach(function(entry){ clusters.push([]) });
    
    for(var j=0;j<data.length;j++){
        var dataPoint = data[j];
        var minDist = distFunc(dataPoint,clusterMeans[0]);
        var minClusterIndex = 0;
        for(var i=0;i<clusterMeans.length;i++){
            var distToMean = distFunc(dataPoint,clusterMeans[i]);
            if( distToMean < minDist ){
                minDist = distToMean;
                minClusterIndex = i;
            }
        }
        clusters[minClusterIndex].push(dataPoint);
    }
    return clusters;    
}

function centroidUpdate(clusters){
    var means =[];
    for(var i=0;i<clusters.length;i++){
        var clusterMeans = [];
        var currCluster = clusters[i];
        for(var featurePos =0;featurePos<currCluster[0].length;featurePos++){
            var newCentroidFeatureMean = mean(feature_vector(currCluster,featurePos));
            clusterMeans.push( newCentroidFeatureMean );
        }
        means.push(clusterMeans);
    }
    return means;
}