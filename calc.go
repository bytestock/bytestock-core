package main

import (
	"fmt"
	"log"
	"math"
	"math/rand"

	"github.com/montanaflynn/stats"
	"gonum.org/v1/gonum/stat/distuv"
)

/*
PLEASE READ:

I have modified the program according to your comments. A few things:

1. The data is hard coded for right now. This will be relatively easy to fix, I just needed to run the program on the exact same values every time to ensure changes in results were from the program, not differing close data.
2. I have changed all mentions of "comparison" to "period".
3. The calculation of probability now runs on every period, and prints out exactly 25 lines (one for each period 5 through 30).
4. I have commented out daily ratios, once everything is working, I will delete them and clean up the entire program.
5. I have changed the weekly ratios to run against the 5th day every time. However, I cannot move this to outside the loop because it depends upon the variable "index". With every iteration of the loop, the index changes, and the data changes as well.
6. I have incorporated the period variable into these calculations.
7. I have updated the val_in_ten_days variable to include the period variable.
8. I am aware of the "mess" the if statements are right now. However, until the program is working 100%, I would like to keep them like this, as it makes it easier to debug. Once everything else is confirmed as working, I will change the if statements.

One other inquiry:

- Upon running the program, the values that are being printed vary pretty significantly, being up to 20% different on each run. Is this expected? To avoid this, should I run the program a couple dozen or hundred times and calculate an average?
*/

	func readLines(path string) ([]float64, error) {
		file, err := os.Open(path)
		if err != nil {
			return nil, err
		}
		defer file.Close()

		var lines []float64
		scanner := bufio.NewScanner(file)
		nums, err := strconv.ParseFloat(scanner.Text(), 64)
		if err != nil {
			log.Fatal(err)
		}
		for scanner.Scan() {
			lines = append(lines, nums)
		}
		return lines, scanner.Err()
	}


func sum(arr []int) float64 {
	sum := 0.0
	for _, valueInt := range arr {
		sum += float64(valueInt)
	}
	return sum
}

func average(array []float64) float64 {
	sum := 0.0

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

	return avg
}

func normalDist(weekly_ratio_average float64, weekly_ratio_standard_deviation float64) float64 {
	// Create a normal distribution

	r := rand.Float64()

	dist := distuv.Normal{
		Mu:    weekly_ratio_average,
		Sigma: weekly_ratio_standard_deviation,
	}.Quantile(r)

	//data := make([]float64, 1e5)

	/*// Draw some random values from the standard normal distribution
	for i := range data {
		data[i] = dist.Rand()
	}*/

	return dist

}

/*
func daily_ratio_calculation(index int, close_data []float64) float64 {
	if index > 0 && index < (len(close_data)-1) {
		daily_ratio := close_data[index-1] / close_data[index]
		return daily_ratio
	}
	return 0.0
}*/

func weekly_ratio_calculation(index int, close_data []float64) float64 {
	weekly_ratio := close_data[index] / close_data[int(math.Abs(float64(index-5)))]

	return weekly_ratio
}

func weekly_ratio_average_calculations(weekly_ratio_values []float64, comparison int) float64 {
	weekly_ratio_average := average(weekly_ratio_values[len(weekly_ratio_values)-comparison : len(weekly_ratio_values)-1])

	return weekly_ratio_average
}

func weekly_ratio_standard_deviation_calculation(weekly_ratio_values []float64, comparison int) float64 {
	weekly_ratio_std, err := stats.StandardDeviation(weekly_ratio_values[len(weekly_ratio_values)-comparison : len(weekly_ratio_values)-1])
	if err != nil {
		log.Fatal(err)
	}

	return weekly_ratio_std
}

func simulation_and_probability_calculations(index int, close_data []float64, weekly_ratio_average float64, weekly_ratio_standard_deviation float64, period int) (int, int) {
	var simulation_values []float64
	true_count := 0
	false_count := 0
	current_simulation_value := close_data[index]
	current_weekly_average := weekly_ratio_average
	current_weekly_standard_deviation := weekly_ratio_standard_deviation

	for x := 0; x <= 2000; x++ {
		simulation := normalDist(current_weekly_average, current_weekly_standard_deviation) * current_simulation_value
		simulation_values = append(simulation_values, simulation)
	}

	simulation_average := average(simulation_values)

	std_dev, err := stats.StandardDeviation(simulation_values)
	if err != nil {
		log.Fatal(err)
	}

	abs_difference := math.Abs(close_data[index] - simulation_average)

	if abs_difference < 1 {
		//std_dev_plus_3 := simulation_average + (std_dev * 3)
		std_dev_plus_2 := simulation_average + (std_dev * 2)
		//std_dev_plus_1 := simulation_average + std_dev
		//std_dev_minus_1 := simulation_average - std_dev
		std_dev_minus_2 := simulation_average - (std_dev * 2)
		//std_dev_minus_3 := simulation_average - (std_dev * 3)

		if len(close_data) > index+period {
			val_in_ten_days := close_data[index+period]

			fmt.Println(val_in_ten_days, std_dev_plus_2, std_dev_minus_2)

			if val_in_ten_days > std_dev_plus_2 {
				true_count += 1
			} else if val_in_ten_days <= std_dev_plus_2 && val_in_ten_days >= std_dev_minus_2 {
				false_count += 1
			} else if val_in_ten_days < std_dev_minus_2 {
				true_count += 1
			}
		}
	}

	return true_count, false_count

}

func main() {
	//close_data := []float64{381.81280517578125, 378.5751647949219, 379.09320068359375, 384.7615661621094, 379.2724914550781, 381.4541931152344, 379.9499206542969, 375.2279357910156, 381.982177734375, 380.9759826660156, 379.37213134765625, 382.30096435546875, 377.9375915527344, 386.6044921875, 386.3853454589844, 389.0950012207031, 394.0162353515625, 395.45074462890625, 396.9848937988281, 396.2576599121094, 390.0015563964844, 387.16241455078125, 394.3748779296875, 399.1068115234375, 398.6784362792969, 398.827880859375, 403.2111511230469, 404.1376037597656, 399.06695556640625, 404.9345703125, 409.2381286621094, 415.1954040527344, 410.7822570800781, 408.2718200683594, 413.6114501953125, 409.0887145996094, 405.542236328125, 406.4886474609375, 411.2604064941406, 411.0711669921875, 412.40606689453125, 406.72772216796875, 405.71160888671875, 397.5726623535156, 397.0247497558594, 399.1366882324219, 394.8729553222656, 396.21783447265625, 394.75341796875, 393.23919677734375, 396.2975158691406, 402.65325927734375, 402.9322204589844, 396.7557678222656, 397.4033203125, 390.0712890625, 384.4427795410156, 383.89483642578125, 390.24066162109375, 387.7999572753906, 394.6039733886719, 389.989990234375, 393.739990234375, 398.9100036621094, 392.1099853515625, 393.1700134277344, 395.75}
	close_data := readLines("close-data.txt")
	//for current_comparison := 0; current_comparison < len(close_data); current_comparison++ {
	var total_true_count []int
	var total_false_count []int
	for period := 5; period <= 30; period++ {
		trues := 0
		falses := 0

		//var daily_ratio_values []float64
		var weekly_ratio_values []float64

		//daily_ratio_values = nil
		weekly_ratio_values = nil
		total_true_count = nil
		total_false_count = nil

		for index := 5; index < len(close_data); index++ {
			//daily_ratio_values = append(daily_ratio_values, daily_ratio_calculation(index, close_data))
			weekly_ratio_values = append(weekly_ratio_values, weekly_ratio_calculation(index, close_data))

			if len(weekly_ratio_values) >= period {
				weekly_ratio_average := weekly_ratio_average_calculations(weekly_ratio_values, period)
				weekly_ratio_standard_deviation := weekly_ratio_standard_deviation_calculation(weekly_ratio_values, period)

				true_count, false_count := simulation_and_probability_calculations(index, close_data, weekly_ratio_average, weekly_ratio_standard_deviation, period)
				trues += true_count
				falses += false_count
				fmt.Println(trues,falses)
			}
		}
		total_true_count = append(total_true_count, trues)
		total_false_count = append(total_false_count, falses)

		fmt.Println(sum(total_true_count), sum(total_false_count))
		fmt.Println("Period: ", period, "Probability: ", (sum(total_true_count)/(sum(total_true_count)+sum(total_false_count)))*100, "%")
		//fmt.Println(len(total_false_count))

	}
}

//}
