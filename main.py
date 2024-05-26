import pandas as pd
import matplotlib.pyplot as plt

class Graph:
        
        def __init__(self,hotel_name):
            self.hotel_name = hotel_name
      
         
        def plotGraph(self, list_city, list_resort , title, xlabel, ylabel):
            print ("---- ",self.hotel_name ,"----")
            print ("\n")
            
            # Plotting the graph
            plt.figure(figsize=(15,5))
            bar_city = plt.bar(list_city.index, list_city, width=0.4, label='City Hotel')
            bar_resort = plt.bar(list_resort.index, list_resort, width=0.4, label='Resort Hotel', align='edge')
            
            for bars in [bar_city, bar_resort]:
                for bar in bars:
                    yval = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom') 

            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.legend()
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
        
    
    def reservation_per_month_n_season(self, hotel_name):
        reservations_per_month = {}
        plot_per_season = {}
        
        for name in hotel_name:
            hotel = self.hotel_booking.loc[self.hotel_booking['hotel'] == name]
            graph = Graph(name)
            
            # Reservations Per Month
            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            reservations_per_month[name] = hotel['arrival_date_month'].value_counts()
            reservations_per_month[name] = reservations_per_month[name].reindex(months)
            # print("Reservations Per Month: ", reservations_per_month)
           
            # Reservation per Season
            seasons = ['Spring', 'Summer', 'Fall', 'Winter']
            
            reservations_per_season = {}
            j = 0
            for i in range(2, 11, 3):
                reservations_per_season[seasons[j]] = reservations_per_month[name].iloc[ i : i+3].sum()
                j += 1
                
            reservations_per_season['Winter'] = reservations_per_month[name].iloc[0:2].sum() + reservations_per_month[name].iloc[11]
            plot_per_season[name] = pd.Series(reservations_per_season)
            
        
        graph.plotGraph(reservations_per_month['City Hotel'], reservations_per_month['Resort Hotel'], "Reservations Per Month", "Months", "Number of Reservations")
        graph.plotGraph(plot_per_season['City Hotel'], plot_per_season['Resort Hotel'], "Reservations Per Season", "Seasons", "Number of Reservations")
        
    def reservation_per_roomtype(self, hotel_name):
        hotel = self.hotel_booking.loc[self.hotel_booking['hotel'] == hotel_name]
        graph = Graph(hotel_name)
        
        # Reservations Per Room Type
        reservations_per_room_type = hotel['reserved_room_type'].value_counts()
        reservations_per_room_type = reservations_per_room_type.sort_index()
        print("Reservations Per Room Type: ", reservations_per_room_type)
        graph.plotGraph(reservations_per_room_type, "Reservations Per Room Type", "Room Type", "Number of Reservations")
        
    def reservation_per_visitortype(self, hotel_name):
        hotel = self.hotel_booking.loc[self.hotel_booking['hotel'] == hotel_name]
        graph = Graph(hotel_name)
        
        # Reservations Per Visitor Type
        alone = hotel.apply(lambda row: row['adults'] == 1 and row['children'] == 0 and row['babies'] == 0, axis=1).sum()
        print("Alone Visitors: ",alone)

        couple = hotel.apply(lambda row: row['adults'] >= 2 and row['children'] == 0 and row['babies'] == 0, axis=1).sum()
        print("Couples: ", couple)

        family = hotel.apply(lambda row: row['adults'] >= 0 and (row['children'] >= 1 or row['babies'] >= 1), axis=1).sum()
        print("Families: ", family)

        notvalid = hotel.apply(lambda row: row['adults'] == 0 and row['children'] == 0 and row['babies'] == 0, axis=1).sum()
        print("Not Valid: ", notvalid)

        total = alone + couple + family + notvalid
        print ("Total: ", total , hotel.shape[0])

        x = ["Alone", "Couple", "Family", "Not Valid"]
        y = [alone, couple, family, notvalid]
        Series = pd.Series(y, index = x)
        
        graph.plotGraph(Series, "Reservations Per Visitor Type", "Visitor Type", "Number of Reservations")

    
    def reservations_per_year(self, hotel_name):
        reservations_per_year = {}
        graph = Graph(hotel_name)
        for name in hotel_name:
            hotel = self.hotel_booking.loc[self.hotel_booking['hotel'] == name]
            
            
            # Reservations Per Year
            reservations_per_year[name] = hotel['arrival_date_year'].value_counts()
            print("Reservations Per Year: ", reservations_per_year)
            
        graph.plotGraph(reservations_per_year['City Hotel'], reservations_per_year['Resort Hotel'] , "Reservations Per Year", "Year", "Number of Reservations")

        
        
        
if __name__ == '__main__':
    file = 'Input/hotel_booking.csv'
    input = Input(file)

    # input.printDataFrame()

    ## 1. Hotel Statistics ##
    
    # #City Hotel
    # input.hotel_statistics('City Hotel')
    
    # #Resort Hotel
    # input.hotel_statistics('Resort Hotel')
    
    # ## 2. Plots Reservations Per Month and Per Season ##
      
    input.reservation_per_month_n_season(['City Hotel', 'Resort Hotel'])
    
    
    
    # ## 3. Plots reservation per Room Type ##
    
    # #City Hotel
    # input.reservation_per_roomtype('City Hotel')
    
    # #Resort Hotel   
    # input.reservation_per_roomtype('Resort Hotel')
    
    
    ## 4. Plots reservation per Customer Type ##
    
    #City Hotel
    # input.reservation_per_visitortype('City Hotel')
    
    # #Resort Hotel   
    # input.reservation_per_visitortype('Resort Hotel')

    ## 5. Plots reservation per Year ##
    input.reservations_per_year(['City Hotel', 'Resort Hotel'] )


    
    