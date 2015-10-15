function prob13_1(datavals,means){
    var classified_points = [];

    for(var j=0;j<means.length;j++){ //num clusters
        classified_points.push([]);
    }

    for(var i=0;i<datavals.length;i++){
        var clusterIndex = 0;
        var minDistToCluster = Number.MAX_SAFE_INTEGER;
        for(var j=0;j<means.length;j++){
            if(Math.abs(datavals[i]-means[j]) < minDistToCluster){
                minDistToCluster = datavals[i]-means[j];
                clusterIndex = j;
            }
        }
        classified_points[clusterIndex].push(datavals[i]);
    }
    var retVal = "After one iteration of K-Means algorithm the data points are classified as follows: </br>";

    for(var j=0;j<classified_points.length;j++){ //num clusters
        retVal+="Original mean ("+means[j]+"):";
        retVal += classified_points[j];
        retVal+="</br>";
    }
    retVal+="</br>"

    for(var j=0;j<classified_points.length;j++){ //num clusters
        retVal+="Original mean ("+means[j]+"). New mean = "+mean(classified_points[j]);
        retVal+="</br>";
    }

    return retVal;
}
