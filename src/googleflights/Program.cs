using System;

namespace googleflights
{
    class Program
    {
        /// <summary>
        /// This example uses the discovery API to list all APIs in the discovery repository.
        /// https://developers.google.com/discovery/v1/using.
        /// <summary>
        [STAThread]
        static void Main(string[] args)
        {
            Console.WriteLine("Discovery API Sample");
            Console.WriteLine("====================");

            FlightSearcher searcer = new FlightSearcher();
            searcer.Search();

            Console.WriteLine("Press any key to continue...");
            Console.ReadKey();
        }

    }
}
