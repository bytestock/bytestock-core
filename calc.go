package main // package main

import ( // import all the libraries needed
	"bufio"
	"fmt"
	"log"
	"math"
	"math/rand"
	"os"
	"strconv"

	"github.com/montanaflynn/stats"
	"gonum.org/v1/gonum/stat/distuv"
)

func readLines(path string) ([]string, error) { // create a function readLines that reads a file and returns the lines read
	file, err := os.Open(path) // open the file and handle the error
	if err != nil {
		return nil, err
	}
	defer file.Close() // close the file once we have the contents read to memory

	var lines []string                // create an array to hold the lines
	scanner := bufio.NewScanner(file) // read the contents of the file
	if err != nil {
		log.Fatal(err)
	}
	for scanner.Scan() { // append each line to lines array
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err() // return the lines read and any errors generated
}

func sum(arr []int) float64 { // create a function that returns the sum of an array
	sum := 0.0                     // create a variable to house the sum
	for _, valueInt := range arr { // loop through the array and add each float to the sum variable
		sum += float64(valueInt)
	}
	return sum // return the sum
}

func average(array []float64) float64 { // create a function that returns the average of an array
	sum := 0.0 // create a variable to house the sum of an array

	// traversing through the
	// array using for loop
	for i := 0; i < len(array); i++ {

		// adding the values of
		// array to the variable sum
		sum += (array[i])
	}

	// declaring a variable
	// avg to find the average
	avg := (float64(sum)) / (float64(len(array)))

	return avg // return the average
}

func normalDist(weekly_ratio_average float64, weekly_ratio_standard_deviation float64) float64 { // create a function to create a normal distribution based on a number of inputs
	// Create a normal distribution

	r := rand.Float64() // create a random 64 bit floating point number

	dist := distuv.Normal{ // use the distuv library to create a normal distribution
		Mu:    weekly_ratio_average,
		Sigma: weekly_ratio_standard_deviation,
	}.Quantile(r)

	return dist // return the value generated

}

func weekly_ratio_calculation(index int, close_data []float64) float64 { // create a function to calculate the weekly ratios
	weekly_ratio := close_data[index] / close_data[int(math.Abs(float64(index-5)))] // calculate the weekly ratio

	return weekly_ratio // return value generated
}

func weekly_ratio_average_calculations(weekly_ratio_values []float64, comparison int) float64 { // create a function to calulate the average weekly ratio
	weekly_ratio_average := average(weekly_ratio_values[len(weekly_ratio_values)-comparison : len(weekly_ratio_values)-1]) // calculate the weekly average ratio

	return weekly_ratio_average // return value generated
}

func weekly_ratio_standard_deviation_calculation(weekly_ratio_values []float64, comparison int) float64 { // create a function to calculate the weekly standard deviation
	weekly_ratio_std, err := stats.StandardDeviation(weekly_ratio_values[len(weekly_ratio_values)-comparison : len(weekly_ratio_values)-1]) // calculate the std_dev and parse the error
	if err != nil {
		log.Fatal(err)
	}

	return weekly_ratio_std // return value generated
}

func simulation_and_probability_calculations(index int, close_data []float64, weekly_ratio_average float64, weekly_ratio_standard_deviation float64, period int) (int, int) { // create a function that runs the main simulation
	var simulation_values []float64 // create an array to house the simulation values
	true_count := 0                 // create variables for true and false counts
	false_count := 0
	current_simulation_value := close_data[index]                        // get the currenty value
	current_weekly_average := weekly_ratio_average                       //  get the current weekly average
	current_weekly_standard_deviation := weekly_ratio_standard_deviation // get the current weekly standard deviation

	for x := 0; x <= 3000; x++ { // run the simulation 3000 times
		simulation := normalDist(current_weekly_average, current_weekly_standard_deviation) * current_simulation_value // run the simulation
		simulation_values = append(simulation_values, simulation)                                                      // append the simulated value to the above array
	}

	simulation_average := average(simulation_values) // calculate the average of the simulation

	std_dev, err := stats.StandardDeviation(simulation_values) // calculate the standard deviation of the simulation
	if err != nil {
		log.Fatal(err)
	}

	abs_difference := math.Abs(close_data[index] - simulation_average) // calculate the absolute difference

	if abs_difference < 1 { // if the difference is less than one, the run the following:
		std_dev_plus_2 := simulation_average + (std_dev * 2)  // calculate what the std plus 2 would be
		std_dev_minus_2 := simulation_average - (std_dev * 2) // calculate what the std minus 2 would be

		if len(close_data) > index+period { // only continue if there are enough values in close data
			val_in_ten_days := close_data[index+period] // check the value in n days

			if val_in_ten_days > std_dev_plus_2 { // if it is outside the std dev plus 2
				true_count += 1
			} else if val_in_ten_days <= std_dev_plus_2 && val_in_ten_days >= std_dev_minus_2 { // if it is within two standard deviations
				false_count += 1
			} else if val_in_ten_days < std_dev_minus_2 { // if it is outside the std dev minus 2
				true_count += 1
			}
		}
	}

	return true_count, false_count // return the true and false count

}

func main() {
	data, err := readLines("close-data.txt") // read the data from close-data
	if err != nil {
		log.Fatal(err)
	}
	var close_data []float64       // create a variable close_data
	for _, element := range data { // loop through the data array
		element, _ := strconv.ParseFloat(element, 64) // convert each line to a float value
		close_data = append(close_data, element)
	}

	var total_true_count []int // create a variable for true and false counts
	var total_false_count []int
	for period := 5; period <= 30; period++ { // loop through a period of 5 to 30 days
		trues := 0 // calculate the trues and falses
		falses := 0

		var weekly_ratio_values []float64 // house the weekly ratio values in an array

		weekly_ratio_values = nil // set all the values to nil
		total_true_count = nil
		total_false_count = nil

		for index := 5; index < len(close_data); index++ { // run a loop over the entire close data list
			weekly_ratio_values = append(weekly_ratio_values, weekly_ratio_calculation(index, close_data)) // append the weekly ratios

			if len(weekly_ratio_values) >= period { // if there are enough values in the list, run the simulation
				weekly_ratio_average := weekly_ratio_average_calculations(weekly_ratio_values, period) // get the average and standard deviation
				weekly_ratio_standard_deviation := weekly_ratio_standard_deviation_calculation(weekly_ratio_values, period)

				true_count, false_count := simulation_and_probability_calculations(index, close_data, weekly_ratio_average, weekly_ratio_standard_deviation, period) // run the simulation
				trues += true_count                                                                                                                                  // add the trues and falses
				falses += false_count
			}
		}
		total_true_count = append(total_true_count, trues)    // add the total true count to the trues
		total_false_count = append(total_false_count, falses) // add the total false count to the falses

		fmt.Println("Period:", period, "Probability:", (sum(total_true_count)/(sum(total_true_count)+sum(total_false_count)))*100, "%") // print the results of the simulation on each period
	}
}
