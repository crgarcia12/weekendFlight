using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace googleflights
{
    class Weekend
    {
        public DateTime Fecha { get; set; }

        public Dictionary<string, Airline> Airlines { get; private set; } = new Dictionary<string, Airline>();
    }
}
