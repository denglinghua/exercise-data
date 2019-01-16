using System;
using System.Collections.Generic;
using System.Text;

namespace RunData
{
    class Logger
    {
        public delegate void Log(string msg);
        private Log log;

        public static Logger Instance;

        public static void Init(Log log)
        {
            Instance = new Logger();
            Instance.log = log;
        }

        public static void info(string msg)
        {
            Instance.log(msg);
        }
    }
}
