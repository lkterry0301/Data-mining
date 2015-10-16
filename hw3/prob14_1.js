//c1,c2 are clusters
function singleLinkMinDist(c1,c2,similarityFunc){
    //transform points into a cluster by wrapping in an array, which makes the dist calculation simpler than a bunch of cases
    if(! (c1[0] instanceof Array)){
        c1 =[c1];
    }
    if(! (c2[0] instanceof Array)){
        c2 = [c2];
    }
    
    //find the min dist btw 2 clusters
    var minDist = Number.MAX_VALUE;
    for(var i=0; i<c1.length;i++){
        for(var j=0; j<c2.length;j++){
            var dist = similarityFunc(c1[i],c2[j]);
            if(dist< minDist){
                minDist = dist;
            }
        }
    }
    
    return minDist;
}

function completeLinkMaxDist(c1,c2,similarityFunc){
    //transform points into a cluster by wrapping in an array, which makes the dist calculation simpler than a bunch of cases
    if(! (c1[0] instanceof Array)){
        c1 =[c1];
    }
    if(! (c2[0] instanceof Array)){
        c2 = [c2];
    }
    
    //find the min dist btw 2 clusters
    var maxDist = Number.MAX_VALUE;
    for(var i=0; i<c1.length;i++){
        for(var j=0; j<c2.length;j++){
            var dist = similarityFunc(c1[i],c2[j]);
            if(dist> maxDist){
                maxDist = dist;
            }
        }
    }
    
    
    return maxDist;
}
function groupAvgDist(c1,c2,similarityFunc){
    //transform points into a cluster by wrapping in an array, which makes the dist calculation simpler than a bunch of cases
    if(! (c1[0] instanceof Array)){
        c1 =[c1];
    }
    if(! (c2[0] instanceof Array)){
        c2 = [c2];
    }
    
    //find the min dist btw 2 clusters
    var totalSum =0;
    for(var i=0; i<c1.length;i++){
        var clusterISum =0;
        for(var j=0; j<c2.length;j++){
            clusterISum += similarityFunc(c1[i],c2[j]);
        }
        totalSum += clusterISum
    }
    
    
    return totalSum / (c1.length * c2.length);
}

function dist_matrix(clusters,similarityFunc,clusterDistFunc){
    var distMatrix = [];
    
    for(var i=0;i<clusters.length;i++){
        distMatrix.push([]);
        
        for(var j=0;j<i;j++){
            distMatrix[i].push(1/0);
        }
        
        for(var j=i;j<clusters.length;j++){
            distMatrix[i].push( clusterDistFunc( clusters[i], clusters[j], similarityFunc));
        }
    }
    
    return distMatrix;
}
function find_merge_point_min(dist_matrix){
    var min = Number.MAX_VALUE;
    var point;
    //search in the top right quadrant
    for(var i=0;i<dist_matrix.length;i++){
        for(var j=i+1;j<dist_matrix[i].length;j++){//cannot merge with itself, so go from i+! to end
            if(dist_matrix[i][j] < min){
                min = dist_matrix[i][j];
                point =[i,j];
            }
        }
    }
    return point;
}

function find_merge_point_max(dist_matrix){
    var max = -Number.MAX_VALUE;
    var point;
    //search in the top right quadrant
    for(var i=0;i<dist_matrix.length;i++){
        for(var j=i+1;j<dist_matrix[i].length;j++){//cannot merge with itself, so go from i+! to end
            if(dist_matrix[i][j] > max){
                max = dist_matrix[i][j];
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

function agglomerativeClustering(points,similarityFunc,clusterDistFunc,mergeFunction){
    var clusters = points.map(function(point){return [point];});
    var cluster_progression = "";
    while(clusters.length > 1){
        cluster_progression += clusteringToString(clusters) +"</br>";
        
        var distMatrix = dist_matrix(clusters,similarityFunc,clusterDistFunc);
        //cluster_progression += prettify_dist_matrix(distMatrix);
        var merge_point = mergeFunction(distMatrix);
        var new_cluster = mergeClusters(clusters[merge_point[0]], clusters[merge_point[1]] );
        
        var firstToSplice = Math.max(merge_point[0],merge_point[1]);
        var secondToSplice = Math.min(merge_point[0],merge_point[1]);
        clusters.splice(firstToSplice,1);
        clusters.splice(secondToSplice,1);
        
        clusters.push(new_cluster);
    }
    cluster_progression += clusteringToString([clusters]) +"</br>";
    return cluster_progression;
}

function mergeClusters(c1,c2){
    if(! (c1[0] instanceof Array)){
        c1 =[c1];
    }
    if(! (c2[0] instanceof Array)){
        c2 = [c2];
    }
    return [c1,c2];
}