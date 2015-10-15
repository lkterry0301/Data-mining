//entropy and splitEntropy functions are in prob19_4.js

function prob19_5(data,dataClasses){
    var retVal = "";
    var split = nonlinearNumericalSplit(data,
        function(dataPoint){
            var a = dataPoint[0];
            var b = dataPoint[1];
            return ( a*b-Math.pow(b,2) ) <= 0;
        });
    retVal += "Split Lesser Data Indices: "+pointToIndices(split[0],data)+"</br>";
    retVal += "Split Greater Data Indices: "+pointToIndices(split[1],data)+"</br>";
    
    var originalClasses = getClassLabels(data,dataClasses);
    var dataE = entropy(originalClasses);
    var splitE = splitEntropy( getClassLabels(split[0],dataClasses),
                              getClassLabels(split[1],dataClasses) );
    
    retVal += "Information Gain: "+dataE +" - "+splitE+" = "+ (dataE-splitE);
    
    return retVal;
}

function pointToIndices(split,originalData){
    var indices =[];
    for(var i=0;i<split.length;i++){
        indices.push(originalData.indexOf(split[i]));
    }
    return indices;
}


function nonlinearNumericalSplit(data,splitFunc){
    var splitLess = [];
    var splitGreater = [];
    
    for(var k=0;k<data.length;k++){
        var dataPoint = data[k];
        if( splitFunc(dataPoint) ){
            splitLess.push(dataPoint);
        }else{
            splitGreater.push(dataPoint);
        }
    }
    return [splitLess,splitGreater];    
}