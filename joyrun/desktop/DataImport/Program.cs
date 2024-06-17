using System;

namespace DataImport
{
    class Program
    {
        static void Main(string[] args)
        {
            Logger.Init(ConsoleWrite);
            new ExcelImport().LoadRunRecord(args[0]);
            //new CalendarSql().GenSql();
        }

        private static void ConsoleWrite(String text)
        {
            Console.WriteLine(text);
        }
    }
}
