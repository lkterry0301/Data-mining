
function EuclideanDist(p1,p2){
    var sum = 0;
    for(var feature=0;feature<p1.length;feature++){
        sum += Math.pow(p2[feature]-p1[feature],2);
    }
    return Math.sqrt(sum);
}

function ManhattanDist(p1,p2){
    var sum = 0;
    for(var feature=0;feature<p1.length;feature++){
        sum += Math.abs(p2[feature]-p1[feature]);
    }
    return sum;
}

function clustersToData(clustersList){
    var data = []
    clustersList.forEach(function(cluster){
        data = data.concat(cluster);
    });
    return data;
}

function clusteringToString(clusters){
    var retVal = "";
    
    clusters.forEach(function(entry){
        retVal += " {"
        
        if(entry[0] instanceof Array){
            retVal += entry.map(function(dataPt){
                //OK, so this is confusing. There is a recursive call if the cluster is itself made up of further clusters (agglomerative clustering)
                var dataOrFurtherClusters = "";
                if(dataPt[0][0] instanceof Array){
                    dataOrFurtherClusters += clusteringToString(dataPt);
                }else{
                    dataOrFurtherClusters= dataPt
                }
                    return " ["+dataOrFurtherClusters+"] ";
                });
        }else{
            retVal += entry;
        }
        
        retVal += "} ";
    });
    
    return retVal;
}

function dataPointsAreEqual(p1,p2){
    if(p1.length !=p2.length){return false;}
    
    for(var i=0;i<p1.length;i++){
        if(p1[i] != p2[i] ){
            return false;
        }
    }
    return true;
}

function mean(values){
    var sum = values.reduce(function(sum, value){
      return sum + value;
    }, 0);

    return sum / values.length;
}

function standardDeviation(values){
    var avg = mean(values);
    
    var sum = values.reduce(function(sum,value){
      var diff = value - avg;
      var sqr = diff * diff;
      return sum+sqr;
    }, 0);
    
    return Math.sqrt(sum / values.length);
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

function feature_vector(data,featurePos){
    var vector = [];
    for(var i=0;i<data.length;i++){
        vector.push(data[i][featurePos]);
    }
    return vector;
}



function contingency_table(p1,p2){
    //iterate thru every attribute
    var num_both_1 = 0;
    var num_both_0 = 0;
    var num_point1_is_0_and_point2_is_1 = 0;
    var num_point1_is_1_and_point2_is_0 = 0;
    for(var i=0;i<p1.length;i++){
        if(p1[i] == p2[i]){
            if(p1[i] == 1){
                num_both_1++;
            }else if(p1[i]==0){
                num_both_0++;
            }
        }else{
            if(p1[i] == 1){
                num_point1_is_1_and_point2_is_0++;
            }else if(p1[i]==0){
                num_point1_is_0_and_point2_is_1++;
            }
        }
    }
    return [num_both_1,
            num_both_0,
            num_point1_is_0_and_point2_is_1,
            num_point1_is_1_and_point2_is_0]
}
function RC_similarity(p1,p2){
    var similarty_table = contingency_table(p1,p2);
    return similarty_table[0]
        /(similarty_table[0]+similarty_table[1]+similarty_table[2]+similarty_table[3]);
}
function SMC_similarity(p1,p2){
    var similarty_table = contingency_table(p1,p2);
    return (similarty_table[0]+similarty_table[1])
        /(similarty_table[0]+similarty_table[1]+similarty_table[2]+similarty_table[3]);
}
function JC_similarity(p1,p2){
    var similarty_table = contingency_table(p1,p2);
    return similarty_table[0]
        /(similarty_table[0]+similarty_table[2]+similarty_table[3]);
}
