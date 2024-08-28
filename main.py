import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk

from Database import Database

class Graph:
        
        def __init__(self,hotel_name):
            self.hotel_name = hotel_name
      
         
        def plotGraph(self, list_city, list_resort , title, xlabel, ylabel, filename):
            # Plotting the graph
            plt.figure(figsize=(15,5))
            bar_city = plt.bar(list_city.index, list_city, width=0.4, label='City Hotel') # City Hotel Blue Bar
            bar_resort = plt.bar(list_resort.index, list_resort, width=0.4, label='Resort Hotel', align='edge') # Resort Hotel Orange Bar
            
            for bars in [bar_city, bar_resort]: # Add the values on top of the bars
                for bar in bars:
                    yval = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom') 

            plt.title(title) # Title of the Graph
            plt.xlabel(xlabel) # X-axis Label
            plt.ylabel(ylabel) # Y-axis Label
            plt.legend() # It categorizes the bars by color
            plt.get_current_fig_manager().set_window_title(title) # Title of the Window
            plt.savefig(filename) # Save the Graph in a file with name from functions' parameter
            
            
        
        def plot_average_stay_days(self, hotel_name, avg_stay_days, avg_actual_stay_days, filename):
            labels = ['Planned', 'Actual']
            values = [avg_stay_days, avg_actual_stay_days]

            plt.figure(figsize=(10, 6))
            plt.bar(labels, values, color=['blue', 'green'])
            plt.xlabel('Type of Stay')
            plt.ylabel('Average Stay Days')
            plt.title(f'Average Stay Days for {hotel_name}')
            plt.savefig(f'{hotel_name}_Average_Stay_Days.png')
            plt.savefig(filename)

        def plot_percentage_cancellations(self, percentage, hotel_name, filename ):
            labels = ['Cancelled', 'Not Cancelled']
            sizes = [percentage, 100 - percentage]
            colors = ['lightcoral', 'lightgreen']
            
            plt.figure(figsize=(8, 6))
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            plt.title(f'Percentage of Cancellations for {hotel_name}')
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.savefig(filename)
            
        
                    


class Input:
    
    def __init__(self, file, db):
        self.hotel_booking = pd.read_csv(file)
        self.db = db
        
    def printDataFrame(self):   
        
        print(self.hotel_booking)

    def averageStayDays(self, hotel):
        # Return the average stay days

        stay_days = hotel['stays_in_weekend_nights'] + hotel['stays_in_week_nights']
        return stay_days.mean()

    def percentageOfCancellations(self, hotel):
        # Return the percentage of cancellations

        total = hotel.shape[0] # .shape[0] returns the number of rows
        canceled = hotel.loc[ hotel['is_canceled'] == 1 ] # .loc[] returns the rows when is_canceled == 1
        total_cancelled = canceled.shape[0]
        return (total_cancelled)/total * 100
    
    def hotel_statistics(self, hotel_name):
        # Creation of a Data Frame that contains only the rows of the hotel_name ('City Hotel', 'Resort Hotel') 
        # Average Stays :  stays_in_weekend_nights + stays_in_week_nights
        # Actual Average Stays : Average Stays but only for reservation that were not canceled
        
        print ("---------------- 1. Hotel Statistics ----------------")
        hotel = self.hotel_booking.loc[self.hotel_booking['hotel'] == hotel_name]
        print ("---- ",hotel_name ,"----")
        print ("\n")
        
        avg_stay_days = self.averageStayDays(hotel)
        print("Average Stay Days that were planned beforehand: " , avg_stay_days)
        
        not_canceled_city = hotel.loc[ hotel['is_canceled'] == 0 ]
        avg_actual_stay_days = self.averageStayDays(not_canceled_city)
        print("Average Stay Days reservations that weren't Cancelled: " , avg_actual_stay_days)
        print ("\n")
        
        
        graph = Graph(hotel_name)
        graph.plot_average_stay_days(hotel_name, avg_stay_days , avg_actual_stay_days, f'1.1 {hotel_name}_Average_Stay_Days.png')
        
        

        
        # Percentage of Cancellations : is_canceled = 1 and percentage = (total_cancelled/total) * 100
        percentage = self.percentageOfCancellations(hotel)
        print("Percentage of cancellations: " , percentage , " %")
        print ("\n")
        
        graph.plot_percentage_cancellations(percentage, hotel_name, f'1.2 {hotel_name}_Percentage_Cancellations.png')
        
        # Save the results in a csv file
        cancelation = pd.DataFrame({
        'Metric': ['Average Stay Days Planned', 'Average Stay Days Actual', 'Percentage of Cancellations'],
        'Value': [avg_stay_days, avg_actual_stay_days, percentage]
        })
        cancelation.to_csv(f'output/1/{hotel_name}_Statistics.csv', index=False, header=True)
        
        # Insert the results in the database
        self.db.insert_hotel_statistics(hotel_name, avg_stay_days, avg_actual_stay_days, percentage)

        
    
    def reservation_per_month_n_season(self, hotel_name, hotel_bk):
        # Input : hotel_name = ['City Hotel', 'Resort Hotel'] => List of Hotel Names
        # For Each Hotel Name: Store the Reservations Per Month and Per Season in a Dictionary
        # Plot the Graphs FROM the Dictionary

        print("---------------- 2. Reservations Per Month and Per Season ----------------")
        
        per_month = {}
        per_season = {}
        
        for name in hotel_name:
            hotel = hotel_bk.loc[ hotel_bk['hotel'] == name]
            
            
            # Reservations Per Month
            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            per_month[name] = hotel['arrival_date_month'].value_counts() # counts every different value in the column ex. [January: 100, February: 200, ... ]
            
            per_month[name] = per_month[name].reindex(months) # changes the index ORDER base on the 'months' list
            
            # Print the results
            print ("---- ",name ,"----")
            print("Reservations Per Month: \n", per_month[name])
            print("\n")
            
            # Reservation per Season
            seasons = ['Spring', 'Summer', 'Fall', 'Winter']
            
            # Categorize every Month to a Season
            # Spring: March, April, May
            # Summer: June, July, August
            # Fall: September, October, November
            rv_per_season = {}
            j = 0
            for i in range(2, 11, 3):
                rv_per_season[seasons[j]] = per_month[name].iloc[ i : i+3].sum()
                j += 1

            # Winter: December, January, February
            # Winter is a special case because indexes Januare and February are in the top of
            # the list per_month[name] and December is in the end   
            rv_per_season['Winter'] = per_month[name].iloc[0:2].sum() + per_month[name].iloc[11]
            per_season[name] = pd.Series(rv_per_season)
            
            #Print the results
            print("Reservations Per Season: \n", per_season[name])
            print("\n")

            # For each month and season, insert the values in the database``
            for season, count in per_season[name].items():
                self.db.insert_reservations_per_season(name, season, count)
            
        # Save the results in a csv file
        per_month['City Hotel'].to_csv('output/2/City_Hotel_Month.csv', header = True)
        per_month['Resort Hotel'].to_csv('output/2/Resort_Hotel_Month.csv', header = True)
        per_season['City Hotel'].to_csv('output/2/City_Hotel_Season.csv', header = True)
        per_season['Resort Hotel'].to_csv('output/2/Resort_Hotel_Season.csv', header = True)
        
        # Plot the Graphs
        graph = Graph(hotel_name)
        graph.plotGraph(per_month['City Hotel'], per_month['Resort Hotel'], "Reservations Per Month", "Months", "Number of Reservations", '2_1.png')
        graph.plotGraph(per_season['City Hotel'], per_season['Resort Hotel'], "Reservations Per Season", "Seasons", "Number of Reservations", '2_2.png')

        
    
    
    def reservation_per_roomtype(self, hotel_name):
        # Input : hotel_name = ['City Hotel', 'Resort Hotel'] => List of Hotel Names
        # For Each Hotel Name: Store the Reservations Per Room Type in a Dictionary
        # Plot the Graphs FROM the Dictionary

        print ("---------------- 3. Reservation Per Room Type ----------------")
        
        per_room_type = {}
        for name in hotel_name:
            hotel = self.hotel_booking.loc[self.hotel_booking['hotel'] == name]
            
            
            # Reservations Per Room Type
            per_room_type[name] = hotel['reserved_room_type'].value_counts() # counts every different value in the column 
            per_room_type[name] = per_room_type[name].sort_index() # sort the index
            print("Reservations Per Room Type: ", per_room_type[name])

            for room_type, count in per_room_type[name].items():
                self.db.insert_reservations_per_room_type(name, room_type, count)
        
        # Save the results in a csv file
        per_room_type['City Hotel'].to_csv('output/3/City_Hotel_Room_Type.csv', header = True)
        per_room_type['Resort Hotel'].to_csv('output/3/Resort_Hotel_Room_Type.csv', header = True)
        
        # Plot the Graphs
        graph = Graph(hotel_name)
        graph.plotGraph(per_room_type['City Hotel'], per_room_type['Resort Hotel'], "Reservations Per Room Type", "Room Type", "Number of Reservations", '3.png')
        
    def reservation_per_visitortype(self, hotel_name):
        # Input : hotel_name = ['City Hotel', 'Resort Hotel'] => List of Hotel Names
        # For Each Hotel Name: Store the Reservations Per Visitor Type in a Dictionary
        # Plot the Graphs FROM the Dictionary
        
        print ("---------------- 4. Reservation Per Visitor Type ----------------")
        
        per_visitor_type = {}
        
        for name in hotel_name:
            hotel = self.hotel_booking.loc[self.hotel_booking['hotel'] == name]
            
            
            # Reservations Per Visitor Type
            alone = hotel.apply(lambda row: row['adults'] == 1 and row['children'] == 0 and row['babies'] == 0, axis=1).sum()
            print("Alone Visitors: ", alone)

            couple = hotel.apply(lambda row: row['adults'] == 2 and row['children'] == 0 and row['babies'] == 0, axis=1).sum()
            print("Couples: ", couple)

            group_adults = hotel.apply(lambda row: row['adults'] > 2 and row['children'] == 0 and row['babies'] == 0, axis=1).sum()
            print("Groups of Adults: ", group_adults)

            family_with_children = hotel.apply(lambda row: row['adults'] >= 1 and row['children'] >= 1 and row['babies'] == 0, axis=1).sum()
            print("Families with Children: ", family_with_children)

            family_with_babies = hotel.apply(lambda row: row['adults'] >= 1 and row['children'] == 0 and row['babies'] >= 1, axis=1).sum()
            print("Families with Babies: ", family_with_babies)

            families_with_both = hotel.apply(lambda row: row['adults'] >= 1 and row['children'] >= 1 and row['babies'] >= 1, axis=1).sum()
            print("Families with Both Children and Babies: ", families_with_both)
            
            
            family = family_with_children + family_with_babies + families_with_both

            children_only = hotel.apply(lambda row: row['adults'] == 0 and row['children'] > 0, axis=1).sum()
            print("Children Only: ", children_only)


            total = alone + couple + family + group_adults + children_only 
            print ("Total: ", total , hotel.shape[0])
            
            notvalid = hotel.shape[0] - total  # No Adults, Children or Babies
            print("Not Valid: ", notvalid)
            
            # Create a Series with the values
            x = ["Alone", "Group of Adults ","Couple", "Family", "Children Only" , "Not Valid"]
            y = [alone, group_adults, couple, family, children_only, notvalid]
            per_visitor_type[name] = pd.Series(y, index = x) # Series is a array in Pandas

            # Insert the values in the database
            for visitor_type, count in per_visitor_type[name].items():
                self.db.insert_reservations_per_visitor_type(name, visitor_type, count)
                
                
        
        # Save the results in a csv file
        per_visitor_type['City Hotel'].to_csv('output/4/City_Hotel_Visitor_Type.csv', header = True)
        per_visitor_type['Resort Hotel'].to_csv('output/4/Resort_Hotel_Visitor_Type.csv', header = True)
        
        # Plot the Graphs
        graph = Graph(name)
        graph.plotGraph(per_visitor_type['City Hotel'], per_visitor_type['Resort Hotel'], "Reservations Per Visitor Type", "Visitor Type", "Number of Reservations", '4.png')

    
    def reservations_per_year(self, hotel_name):
        # Input : hotel_name = ['City Hotel', 'Resort Hotel'] => List of Hotel Names
        # For Each Hotel Name: Store the Reservations Per Year and Per Month Year in a Dictionary
        # Plot the Graphs FROM the Dictionary
        
        print ("---------------- 5. Reservation Per Year ----------------")
        
        per_year = {}
        per_mon_year = {}
        per_year_Unioned_Months = {}
        graph = Graph(hotel_name)
        
        for name in hotel_name:
            hotel = self.hotel_booking.loc[self.hotel_booking['hotel'] == name]
            
            # Reservations Per Year
            # ex [2015: 100, 2016: 200, ... ]
            hotel_per_year = hotel['arrival_date_year']
            per_year[name] =hotel_per_year.value_counts() # counts every different value in the column 
            
            #Print Results
            print ("---- ",name ,"----")
            print("Reservations Per Year: ", per_year)
            print("\n")
            
            # Reservation Per Month in Year
            months_per_year_list = []
            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            
            for year in [2015, 2016, 2017]:
                in_year = hotel.loc[hotel['arrival_date_year'] == year]
                months_in_year = in_year['arrival_date_month'].value_counts() #Counts Reservation Per Month in a Year
                months_in_year = months_in_year.reindex(months)
                
                # Names the object pandas Series with the Year so when I add it in the list 
                # It doesn't get overwritten !!
                months_in_year.name = year
                months_per_year_list.append(months_in_year) # Append the Series in the List
            
            # Combine the monthly data into a single DataFrame
            per_mon_year[name] = pd.concat(months_per_year_list, axis=1).fillna(0).astype(int)

            #Print Results
            print("Reservations Per Month in Year: \n", per_mon_year[name])
            print("\n")
            
             # Insert the values in the database only for Yearly Increase
            for year, count in per_year[name].items():
                self.db.insert_reservations_per_year(name, year, count)
             
                
            # Reservation only for the UNION of the 3 years
            # I notice from the previous data that only July and August
            # are the months that have reservations in all 3 years
            
            union_per_year_2015 = months_per_year_list[0].loc[['July', 'August']].sum()
            union_per_year_2016 = months_per_year_list[1].loc[['July', 'August']].sum()
            union_per_year_2017 = months_per_year_list[2].loc[['July', 'August']].sum()
            
            per_year_Unioned_Months[name] = pd.Series([union_per_year_2015, union_per_year_2016, union_per_year_2017], index = [2015, 2016, 2017])
                
                
        # Save the results in a csv file
        per_year['City Hotel'].to_csv('output/5/City_Hotel_Year.csv', header = True)
        per_year['Resort Hotel'].to_csv('output/5/Resort_Hotel_Year.csv', header = True)
        per_mon_year['City Hotel'].to_csv('output/5/City_Hotel_Month_Year.csv', header = True)
        per_mon_year['Resort Hotel'].to_csv('output/5/Resort_Hotel_Month_Year.csv', header = True)
            
        # Plot the Graphs
        # Yearly Increase    
        graph.plotGraph(per_year['City Hotel'], per_year['Resort Hotel'] , "Reservations Per Year", "Year", "Number of Reservations", '5.png')
        
        # Monthly Increase in every Year
        for i, year in enumerate([2015, 2016, 2017]):
            graph.plotGraph(per_mon_year['City Hotel'][year], per_mon_year['Resort Hotel'][year], f"Reservations Per Month in Year {year}", "Month", "Number of Reservations", f'5_{year}.png')
        
        
        # Union of the 3 years
        graph.plotGraph(per_year_Unioned_Months['City Hotel'], per_year_Unioned_Months['Resort Hotel'], "Reservations Per Year for July and August", "Year", "Number of Reservations", '5_Union.png')
        
    def cancelation_per_month(self, hotel_name):
        # Input : hotel_name = ['City Hotel', 'Resort Hotel'] => List of Hotel Names
        # For Each Hotel Name: Store the Cancelations Per Month in a Dictionary
        # Plot the Graphs FROM the Dictionary
        
        print ("---------------- 6. Cancelation Per Month ----------------")
        per_month = {}
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        for name in hotel_name:
            hotel = self.hotel_booking.loc[self.hotel_booking['hotel'] == name]
            
            # Cancelations Per Month
            canceled = hotel.loc[ hotel['is_canceled'] == 1 ]
            per_month[name] = canceled['arrival_date_month'].value_counts()
            per_month[name] = per_month[name].reindex(months)
        
            # Print the results
            print ("---- ",name ,"----")
            print("Cancelations Per Month: \n", per_month[name])
            print("\n")

        #Plot the Graphs
        garph = Graph(hotel_name)
        garph.plotGraph(per_month['City Hotel'], per_month['Resort Hotel'], "Cancelations Per Month", "Months", "Number of Cancelations", '6.png')

class GUI:
    
    def __init__(self , file,db, window):
        
        # Create the main application window

        # Create the input object
        self.input = Input(file, db)
        self.db = db
        
        # Create and pack the buttons -> Call the Methods of Button Class
        button1 = tk.Button(window, text=f"1. Hotel Statistics", command = self.Button_1 )
        # Align the button to the left
        button1.pack(fill='x', padx=10, pady=5)
         
        button2 = tk.Button(window, text=f"2. Reservations Per Month and Per Season", command = self.Button_2 )
        button2.pack(fill='x', padx=10, pady=5)
         
        button3 = tk.Button(window, text=f"3. Reservation Per Room type", command = self.Button_3)
        button3.pack(fill='x', padx=10, pady=5)
        
        button4 = tk.Button(window, text=f"4. Reservation Per Visitor", command = self.Button_4)
        button4.pack(fill='x', padx=10, pady=5)

        button5 = tk.Button(window, text=f"5. Reservation Per Year", command = self.Button_5)
        button5.pack(fill='x', padx=10, pady=5)
        
        button6 = tk.Button(window, text=f"6. Cancelation per Month", command=self.Button_6)
        button6.pack(fill='x', padx=10, pady=5)
        
        button_db = tk.Button(window, text=f"Export Data Base =Schema", command=self.export_schema)
        button_db.pack(fill='x', padx=10, pady=5)
    
    # The Button Methods that will be called when the buttons are clicked
    # Each button will call a function from the Input Class    
    def Button_1(self):
           self.input.hotel_statistics('City Hotel')
           self.input.hotel_statistics('Resort Hotel')
           
    def Button_2(self):
           self.input.reservation_per_month_n_season(['City Hotel', 'Resort Hotel'], self.input.hotel_booking)  
           
    def Button_3(self):
           self.input.reservation_per_roomtype(['City Hotel', 'Resort Hotel'])
           
    def Button_4(self):
        self.input.reservation_per_visitortype(['City Hotel', 'Resort Hotel'])
    
    def Button_5(self):
        self.input.reservations_per_year(['City Hotel', 'Resort Hotel'] )
        
    def Button_6(self):
        self.input.cancelation_per_month(['City Hotel', 'Resort Hotel'])
        
    def export_schema(self):
        self.db.export_schema()    
        
if __name__ == '__main__':
    file = 'Input/hotel_booking.csv'
    db = Database('hotel_bookings.db')

    input = Input(file, db)
    
    window = tk.Tk()
    window.title("Python Project")
    gui = GUI(file, db, window)
    
    window.mainloop()
    # input.printDataFrame()

    # # 1. Hotel Statistics ##
    
    # #City Hotel
    # input.hotel_statistics('City Hotel')
    
    # #Resort Hotel
    # input.hotel_statistics('Resort Hotel')
    
    # ## 2. Plots Reservations Per Month and Per Season ##
      
    # input.reservation_per_month_n_season(['City Hotel', 'Resort Hotel'])
    
    
    
    # ## 3. Plots reservation per Room Type ##
    
    # input.reservation_per_roomtype(['City Hotel', 'Resort Hotel'])
    
    
    # # 4. Plots reservation per Customer Type ##
    
    # input.reservation_per_visitortype(['City Hotel', 'Resort Hotel'])
    
   

    # ## 5. Plots reservation per Year ##
    # input.reservations_per_year(['City Hotel', 'Resort Hotel'] )


    
    