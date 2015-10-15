function min_max_normalization(data){
    var min = min_val(data);
    var max = max_val(data);
    
    var new_data = [];
    for(var i=0;i<data.length;i++){
        new_data.push( (data[i]-min)/(max-min) );
    }
    return new_data;
}

function normalize_third_feature(newPoint,data){
    //normalize the third feature
    var thirdFeatureValues = [];
    for(var i=0;i<data.length;i++){
        thirdFeatureValues.push(data[i][2]);
    }
    thirdFeatureValues.push(newPoint[2]);
    
    //overwrite third feature values to normalized values
    var normalizedThirdFeature = min_max_normalization(thirdFeatureValues);
    newPoint[2] = normalizedThirdFeature[normalizedThirdFeature.length-1];
    for(var i=0;i<data.length;i++){
        data[i][2] = normalizedThirdFeature[i];
    }    
}

function pointDistances(newPoint,data){
    //reassign third values of newPoint and data based upon min-max normalization
    normalize_third_feature(newPoint,data);
    
    //compute distances
    var distances = [];
    for(var i=0;i<data.length;i++){
        distances.push(EuclideanDist(newPoint,data[i]));
    }
    return distances;
}

function min_val(arr){
    var min = Number.MAX_VALUE;
    for(var i=arr.length-1;i>=0;i--){
        if(arr[i] < min){
            min = arr[i];
        }
    }
    return min;
}

function max_val(arr){
    var max = -Number.MAX_VALUE;
    for(var i=arr.length-1;i>=0;i--){
        if(arr[i] >max){
            max = arr[i];
        }
    }
    return max;
}

function EuclideanDist(p1,p2){
    var sum = 0;
    for(var feature=0;feature<p1.length;feature++){
        sum += Math.pow(p2[feature]-p1[feature],2);
    }
    return Math.sqrt(sum);
}