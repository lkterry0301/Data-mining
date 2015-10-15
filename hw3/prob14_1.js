
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


//c1,c2 are clusters
function singleLinkMinDist(c1,c2,similarityFunc){
    var minDist = Number.MAX_VALUE;
    if(c1[0] instanceof Array){
        for(var i=0; i<c1.length;i++){
            var c1_point = c1[i];
            if(c2[0] instanceof Array){
                for(var j=0; j<c2.length;j++){
                    var c2_point = c2[i];
                    var dist = similarityFunc(c1_point,c2_point);
                    if(dist< minDist){
                        minDist = dist;
                    }
                }
            }else{
                var c2_point = c2;
                var dist = similarityFunc(c1_point,c2_point);
                if(dist< minDist){
                    minDist = dist;
                }
            }
        }
    }else{
        var c1_point = c1;
        if(c2[0] instanceof Array){
            for(var j=0; j<c2.length;j++){
                var c2_point = c2[i];
                var dist = similarityFunc(c1_point,c2_point);
                if(dist< minDist){
                    minDist = dist;
                }
            }
        }else{
            var c2_point = c2;
            var dist = similarityFunc(c1_point,c2_point);
            if(dist< minDist){
                minDist = dist;
            }
        }
    }
    return minDist;
}

function dist_matrix(clusters,similarityFunc,clusterDistFunc){
    var distMatrix = [];
    for(var i=0;i<clusters.length;i++){
        distMatrix.push([]);
        for(var j=clusters.length-1;j>=i;j--){
            distMatrix[i].push(clusterDistFunc( clusters[i], clusters[j], similarityFunc));
        }
    }
    return distMatrix;
}

function find_merge_point_min(dist_matrix){
    var min = Number.MAX_VALUE;
    var point;
    for(var i=0;i<dist_matrix.length;i++){
        for(var j=dist_matrix[i].length-1;j>i;j--){
            if(dist_matrix[i][j] < min){
                min = dist_matrix[i][j];
                point =[i,j];
            }
        }
    }
    return point;
}

function prettify_dist_matrix(dist_matrix){
    var dist_matrixHTML = "<table>"
    for(var i=0;i<dist_matrix.length;i++){
        dist_matrixHTML+="<tr>";
        for(var j=0;j<dist_matrix.length;j++){
            dist_matrixHTML+="<td>"+dist_matrix[i][j]+"</td>";
        }
        dist_matrixHTML+="</tr>";
    }
    dist_matrixHTML+="</table>";
    return dist_matrixHTML;
}

function build_dendogram(points,similarityFunc,clusterDistFunc,mergeFunction){
    var clusters = [points];
    var cluster_progression = "";
    while(clusters.length > 1){
        cluster_progression += clusters +"</br>";
        
        var dist_matrix = dist_matrix(clusters,similarityFunc,clusterDistFunc);
        var merge_point = mergeFunction(dist_matrix);
        var new_cluster = [clusters[merge_point[0]],clusters[merge_point[1]]]
        clusters.remove(merge_point[0]);
        clusters.remove(merge_point[1]);
        
        clusters.add(new_cluster);
    }
    return cluster_progression;
}