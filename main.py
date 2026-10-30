
import api
import charts
import inputs


def main():
    print("Stock Data Visualizer")
    print("---------------------")
    while True:
        symbol = inputs.get_symbol()
        chart_type = inputs.get_chart_type()
        function, series_label = inputs.get_time_series()
        start, end = inputs.get_date_range()

        try:
            series = api.fetch_stock_data(symbol, function)
            rows = api.filter_by_date(series, start, end)
        except api.StockDataError as exc:
            print(f"\nError: {exc}\n")
        else:
            chart = charts.build_chart(rows, symbol, chart_type,
                                       series_label, start, end)
            path = charts.open_in_browser(chart)
            print(f"\nChart opened in your browser ({path}).")

        again = input("\nView more stock data? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
