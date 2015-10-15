function print_car_data_calcs(carClassData, newPoint){
    var retVal="";
    
    retVal += " Mean is "+mean(carClassData)+", stdDev is "+standardDeviation(carClassData)+".";
    retVal += " Probability is "+probability_density_func_for_normal_distribution(carClassData,newPoint)+".";   
    
    return retVal;
}

function probability_density_func_for_normal_distribution(values,num){
    var stdDev = standardDeviation(values);
    var avg = mean(values);
    
    var coefficient = 1/(stdDev * Math.sqrt(2*Math.PI) );
    var power = -1 * Math.pow( num-avg ,2)/ (2*Math.pow(stdDev,2));
    
    return coefficient * Math.pow(Math.E,power) ||0;
}

function standardDeviation(values){
    var summation = sqrDiffSum(values);
    
    return Math.sqrt(summation / values.length);
}

function mean(values){
    var sum = values.reduce(function(sum, value){
      return sum + value;
    }, 0);

    return sum / values.length;
}

function sqrDiffSum(values){
    var avg = mean(values);
    
    var sum = values.reduce(function(sum,value){
      var diff = value - avg;
      var sqr = diff * diff;
      return sum+sqr;
    }, 0);
    
    return sum;
}