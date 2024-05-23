import pandas as pd
import matplotlib.pyplot as plt

class Graph:
        
        def __init__(self,hotel_name):
            self.hotel_name = hotel_name
      
         
        def plotGraph(self, list, title, xlabel, ylabel):
            print ("---- ",self.hotel_name ,"----")
            print ("\n")
            
            # Plotting the graph
            plt.figure(figsize=(15,5))
            bars = plt.bar(list.index, list)
            
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom') 

            plt.title(self.hotel_name + ": " + title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()
            
            print ("\n")


class Input:
    
    def __init__(self, file):
        self.hotel_booking = pd.read_csv(file)
        
    def printDataFrame(self):   
        print(self.hotel_booking)

    def averageStayDays(self, hotel):
        stay_days = hotel['stays_in_weekend_nights'] + hotel['stays_in_week_nights']
        return stay_days.mean()

    def percentageOfCancellations(self, hotel):
        total = hotel.shape[0]
        not_canceled = hotel.loc[ hotel['is_canceled'] == 1 ]
        total_cancelled = not_canceled.shape[0]
        return (total_cancelled)/total * 100
    
    def hotel_statistics(self, hotel_name):
        hotel = self.hotel_booking.loc[self.hotel_booking['hotel'] == hotel_name]
        print ("---- ",hotel_name ,"----")
        print ("\n")
        
        avg_stay_days = self.averageStayDays(hotel)
        print("Average Stay Days that were planned beforehand: " , avg_stay_days)
        
        not_canceled_city = hotel.loc[ hotel['is_canceled'] == 0 ]
        avg_actual_stay_days = self.averageStayDays(not_canceled_city)
        print("Average Stay Days reservations that weren't Cancelled: " , avg_actual_stay_days)
        print ("\n")
        # Percentage of cancellations
        percentage = self.percentageOfCancellations(hotel)
        print("Percentage of cancellations: " , percentage , " %")
        print ("\n")
        
    
    def hotel_plots(self, hotel_name):
        hotel = self.hotel_booking.loc[self.hotel_booking['hotel'] == hotel_name]
        graph = Graph(hotel_name)
        
        # Reservations Per Month
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        reservations_per_month = hotel['arrival_date_month'].value_counts()
        reservations_per_month = reservations_per_month.reindex(months)
        # print("Reservations Per Month: ", reservations_per_month)
        graph.plotGraph(reservations_per_month, "Reservations Per Month", "Months", "Number of Reservations")
        
        # Reservation per Season
        seasons = ['Spring', 'Summer', 'Fall', 'Winter']
        
        reservations_per_season = {}
        j = 0
        for i in range(2, 11, 3):
            reservations_per_season[seasons[j]] = reservations_per_month.iloc[ i : i+3].sum()
            j += 1
            
        reservations_per_season['Winter'] = reservations_per_month.iloc[0:2].sum() + reservations_per_month.iloc[11]
        print("Reservations Per Season: ", reservations_per_season)
        
        graph.plotGraph(pd.Series(reservations_per_season), "Reservations Per Season", "Seasons", "Number of Reservations")
        
        
if __name__ == '__main__':
    file = 'Input/hotel_booking.csv'
    input = Input(file)

    # input.printDataFrame()

    ## 1. Hotel Statistics ##
    
    #City Hotel
    input.hotel_statistics('City Hotel')
    
    #Resort Hotel
    input.hotel_statistics('Resort Hotel')
    
    ## 2. Hotel Plots ##
    
    #City Hotel
    input.hotel_plots('City Hotel')
    
    #Resort Hotel   
    input.hotel_plots('Resort Hotel')
    
    
    
    