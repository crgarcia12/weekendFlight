using Google.Apis.QPXExpress.v1;
using Google.Apis.QPXExpress.v1.Data;
using Google.Apis.Services;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace googleflights
{
    class FlightSearcher
    {
        public void Search()
        {
            List<Weekend> weekends = new List<Weekend>();

            DateTime firstFriday = new DateTime(2017, 04, 28);
            TimeOfDayRange outboundRange = new TimeOfDayRange();
            outboundRange.EarliestTime = "18:00";

            for (int weekendNumber = 0; weekendNumber <= 20; weekendNumber++)
            {
                var weekend = new Weekend()
                {
                    Fecha = firstFriday.AddDays(7 * weekendNumber)
                };

                weekends.Add(weekend);
                QPXExpressService service = new QPXExpressService(new BaseClientService.Initializer() { ApiKey = "AjIzaSyCPh2pXGIj2D8PmqokX4NgGWVThq4-MqAo", ApplicationName = "Daimto QPX Express Sample", });

                TripsSearchRequest x = new TripsSearchRequest(); x.Request = new TripOptionsRequest();
                x.Request.Passengers = new PassengerCounts { AdultCount = 1 };
                x.Request.Slice = new List<SliceInput>();

                x.Request.Slice.Add(new SliceInput()
                {
                    Origin = "CPH",
                    Destination = "ZRH",
                    Date = weekend.Fecha.ToString("yyyy-MM-dd"),  //"2015-10-29"
                    PermittedDepartureTime = outboundRange,
                    MaxConnectionDuration = 300,
                });
                x.Request.Slice.Add(new SliceInput()
                {
                    Origin = "ZRH",
                    Destination = "CPH",
                    Date = weekend.Fecha.AddDays(2).ToString("yyyy-MM-dd"),  //"2015-10-29"
                    PermittedDepartureTime = outboundRange,
                    MaxConnectionDuration = 300,
                });

                x.Request.Solutions = 100;
                var result = service.Trips.Search(x).Execute();

                foreach (var trip in result.Trips.TripOption)
                {
                    string airlineName = trip.Slice.FirstOrDefault().Segment.FirstOrDefault().Flight.Carrier;

                    Airline cheapestFlight;
                    int tripPrice = extractPrice(trip.Pricing.FirstOrDefault().SaleTotal);
                    if (weekend.Airlines.TryGetValue(airlineName, out cheapestFlight))
                    {
                        if (!(tripPrice < cheapestFlight.Price))
                        {
                            continue;
                        }
                    }

                    cheapestFlight = new Airline()
                    {
                        Name = airlineName,
                        Price = tripPrice
                    };

                    weekend.Airlines[cheapestFlight.Name] = cheapestFlight;

                    /*
                    string tripCsv = string.Format("{0},{1},", 
                    tripFriday.ToString("yyyy-MM-dd"), 
                    trip.Pricing.FirstOrDefault().SaleTotal);

                    foreach (var slice in trip.Slice)
                    {
                        tripCsv += string.Format("{0},{1},{2}",
                            slice.Segment.FirstOrDefault().Leg.FirstOrDefault().DepartureTime,
                            slice.Segment.FirstOrDefault().Flight.Carrier,
                            slice.Duration
                         );
                    }
                    Console.WriteLine(tripCsv);
                  */
                }
            }
            printTable(weekends);
        }
 
        private int extractPrice(string price)
        {
            return Int32.Parse(price.Substring(3));
        }

        private void printTable(List<Weekend> weekends)
        {
            Dictionary<string,string> allAirlines = new Dictionary<string, string>();

            foreach(Weekend weekend in weekends)
            {
                foreach(string airline in weekend.Airlines.Keys)
                {
                    if(!allAirlines.ContainsKey(airline))
                    {
                        allAirlines[airline] = airline;
                    }
                }
            }

            // All rows
            List<string> rows = new List<string>();

            // Headers
            StringBuilder row = new StringBuilder("Weekend");
            foreach (string airlineName in allAirlines.Keys)
            {
                row.Append($",{airlineName}");
            }
            rows.Add(row.ToString());

            // Add rows
            foreach (Weekend weekend in weekends)
            {
                row = new StringBuilder(weekend.Fecha.ToString("yyyy-MM-dd"));

                foreach (string airline in allAirlines.Keys)
                {
                    if (weekend.Airlines.ContainsKey(airline))
                    {
                        row.AppendFormat(",{0}", weekend.Airlines[airline].Price); 
                    }
                    else
                    {
                        row.AppendFormat(",");
                    }
                }

                rows.Add(row.ToString());
            }

            foreach (string r in rows)
            {
                Console.WriteLine(r);
            }
        }
    }
}
