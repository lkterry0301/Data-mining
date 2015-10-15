function allSplitsForOriginalDataMatrix(data,data_with_classes){    
    var retVal="";
    
    retVal += "Splitting using Entropy: </br></br>"+originalDataMatrixSplit(data,data_with_classes,splitEntropy)+"</br></br></br>";
    retVal += "Splitting using GINI: </br>"+originalDataMatrixSplit(data,data_with_classes,splitGINI)+"</br></br></br>";
    retVal += "Splitting using CART: </br>"+originalDataMatrixSplit(data,data_with_classes,splitCART)+"</br></br></br>";    
    
    return retVal;
}

//original matrix has 3 features: a1, a2, a3
function originalDataMatrixSplit(data,data_with_classes,evalFunc){    
    var retVal="";
    
    //perform splits on each feature
    retVal += "   Splitting on attribute a1</br>";
    var splits = allSplitsForFeature(data,0,"categorical");
    var splitPoints = splitPointsCategorical(data,0);
    var splitsVals = splitsValues(splits,data_with_classes,evalFunc);
    retVal += SplitResultString(splitPoints,splitsVals);
    
    retVal += "   Splitting on attribute a2</br>";
    splits = allSplitsForFeature(data,1,"categorical");
    splitPoints = splitPointsCategorical(data,1);
    splitsVals = splitsValues(splits,data_with_classes,evalFunc);
    retVal += SplitResultString(splitPoints,splitsVals);
    
    retVal += "   Splitting on attribute a3</br>";
    splits = allSplitsForFeature(data,2,"numerical");
    splitPoints = splitPointsNumerical(data,2);
    splitsVals = splitsValues(splits,data_with_classes,evalFunc);
    retVal += SplitResultString(splitPoints,splitsVals);
    
    retVal += "</br>"
    return retVal;    
}
function SplitResultString(splitPoints,splitVals){
    var retVal ="";
    retVal += "Split values are "+splitPoints+"</br>";
    for(var i=0;i<splitPoints.length;i++){
        retVal += " Split Val of "+splitPoints[i]+" yields "+splitVals[i]+"</br>";
    }
    return retVal;
}

function splitsValues(splits,dataClasses,evalFunc){
    var splitsVals = []
    for(var i=0;i<splits.length;i++){
        //transform the splits, which are of data points, to class label arrays for the eval function
        var class_labels1 = getClassLabels(splits[i][0],dataClasses);
        var class_labels2 = getClassLabels(splits[i][1],dataClasses);
        
        splitsVals.push( evalFunc(class_labels1,class_labels2) );
    }
    return splitsVals;
}

function getClassLabels(split, originalDataClasses){
    return split.map(function(entry) { return originalDataClasses[entry]; });
}

function allSplitsForFeature(data,currFeatureIndex,dataType){
    var allSplits =[];
    
    var splitPointFunc = '';
    var splitFunc = '';
    if(dataType =="categorical"){
        splitPointFunc = splitPointsCategorical;
        splitFunc = categoricalSplit;
    }else{//dataType =="numerical"
        splitPointFunc = splitPointsNumerical;
        splitFunc = numericalSplit;
    }
    
    var splitPoints = splitPointFunc(data,currFeatureIndex);
    for(var j=0;j<splitPoints.length;j++){
        var split = splitFunc(data,currFeatureIndex,splitPoints[j]);
        allSplits.push(split);
    }
    return allSplits;
}

function numericalSplit(data,currFeatureIndex,valueToSplitOn){
    var splitLess = []
    var splitGreater = []
    for(var k=0;k<data.length;k++){
        var dataPoint = data[k];
        if(dataPoint[currFeatureIndex] < valueToSplitOn){
            splitLess.push(dataPoint);
        }else{
            splitGreater.push(dataPoint);
        }
    }
    return [splitLess,splitGreater];    
}

function categoricalSplit(data,currFeatureIndex,valueToSplitOn){
    var splitLess = []
    var splitGreater = []
    for(var k=0;k<data.length;k++){
        var dataPoint = data[k];
        if(dataPoint[currFeatureIndex] == valueToSplitOn){
            splitLess.push(dataPoint);
        }else{
            splitGreater.push(dataPoint);
        }
    }
    return [splitLess,splitGreater];    
}

function performSplit(data,dataClasses,splitFunc,splitPoints,feature_vector){
    var splitVals = []
    for(var j=0;j<splitPoints.length;j++){//perform a split at each possible point
        var splitLess = []
        var splitGreater = []
        for(var k=0;k<feat_vec.length;k++){//separate the class labels in the split into the 2 new arrays
            var dataPoint = data[k];//k is the index in feat_vec, which corresponds to the index in data
            if(feat_vec[k] < splitPoints[j]){//add the class label to respective array
                splitLess.push(data_with_classes[dataPoint]);
            }else{
                splitGreater.push(data_with_classes[dataPoint]);
            }
        }

        var splitVal = splitFunc(splitLess,splitGreater);
        spliVals.push([splitPoints[j],splitVal]);
    }
    return splitVals;
}

function feature_vector(data,featurePos){
    var vector = [];
    for(var i=0;i<data.length;i++){
        vector.push(data[i][featurePos]);
    }
    return vector;
}

function splitEntropy(class_labels1,class_labels2){
    var totalLen = class_labels1.length+class_labels2.length;
    return (class_labels1.length/totalLen) * entropy(class_labels1) + (class_labels2.length/totalLen) * entropy(class_labels2);
}

function splitGINI(class_labels1,class_labels2){
    var totalLen = class_labels1.length+class_labels2.length;
    return (class_labels1.length/totalLen) * GINI(class_labels1) + (class_labels2.length/totalLen) * GINI(class_labels2);
}

function entropy(class_labels){
    var classCounts = classLabelCounts(class_labels);
    
    var classes = Object.keys(classCounts);
    var sum = 0;
    //iterate thru every class
    for(var i=0;i<classes.length;i++){
        //mult the prob of class by the log of inverse prob and add to sum
        var probabilityOfClass = classCounts[classes[i]]/class_labels.length;
        sum += probabilityOfClass * Math.log2(1/probabilityOfClass);
    }
    return sum;
}

function GINI(class_labels){
    var classCounts = classLabelCounts(class_labels);
    
    var classes = Object.keys(classCounts);
    var sum = 0;
    //iterate thru every class
    for(var i=0;i<classes.length;i++){
        //square prob of class add to sum
        var probabilityOfClass = classCounts[classes[i]]/class_labels.length;
        sum += Math.pow(probabilityOfClass,2);
    }
    return 1-sum;
}

function splitCART(class_labels1,class_labels2){
    var classCounts1 = classLabelCounts(class_labels1);
    var classCounts2 = classLabelCounts(class_labels2);
    
    var classes = uniqueItemsArray( Object.keys(classCounts1).concat( Object.keys(classCounts2) ) );
    var sum = 0;
    //iterate thru every class
    for(var i=0;i<classes.length;i++){
        var probClassInData1 = classCounts1[classes[i]]/class_labels1.length || 0;//if a class is not found in the countsHash, set the value to 0
        var probClassInData2 = classCounts2[classes[i]]/class_labels2.length || 0;
        sum += Math.abs(probClassInData1 - probClassInData2);
    }
    var totalLen = class_labels1.length+class_labels2.length;
    return 2 * (class_labels1.length/totalLen) * (class_labels2.length/totalLen) * sum;
}


function classLabelCounts(class_labels){
    //count how many times the class labels occur in the passed list
    var hash = {};
    for(var i=0;i<class_labels.length;i++){
        if(typeof hash[class_labels[i]] !== 'undefined'){
            hash[class_labels[i]] = hash[class_labels[i]] + 1;
        }else{
            hash[class_labels[i]] = 1;
        }
    }
    return hash;
}

function uniqueItemsArray(arr){
    var mySet = new Set();
    
    for(var i=0;i<arr.length;i++){
        mySet.add(arr[i]);
    }
    
    return Array.from(mySet);
}

function splitPointsNumerical(data, featurePos){
    var featureVector = feature_vector(data,featurePos);
    featureVector.sort(function(a,b) { return a - b; });
    
    var splitPoints =[]; //midpoints btw 2 successive values
    for(var i=0;i<featureVector.length-1;i++){
        var split = (featureVector[i]+featureVector[i+1])/2;
        splitPoints.push(split);
    }
    return splitPoints;
}
        
function splitPointsCategorical(data, featurePos){
    var featureVector = feature_vector(data,featurePos);
    return uniqueItemsArray(featureVector);
}

