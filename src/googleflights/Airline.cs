using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace googleflights
{
    class Airline
    {
        public string Name { get; set; }
        public int Price { get; set; }
        public List<Leg> Legs { get; set; } = new List<Leg>();

    }
}
