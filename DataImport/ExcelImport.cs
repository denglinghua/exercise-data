using System;
using System.Collections.Generic;
using System.IO;

using NPOI.SS.UserModel;

namespace DataImport
{
    class ExcelImport
    {
        Dictionary<RunData, RunData> checkDuplicate = new Dictionary<RunData, RunData>();
        List<string> sqls = new List<string>();

        public void LoadRunRecord(string dir)
        {
            checkDuplicate.Clear();
            sqls.Clear();

            string[] files = Directory.GetFiles(dir);
            foreach (string file in files)
            {
                LoadOneFileRunRecord(file);
            }

            File.WriteAllText("run_data.sql", string.Join(Environment.NewLine, sqls.ToArray()));
        }

        public void LoadOneFileRunRecord(string fileName)
        {
            Logger.Info("Load data from file : " + fileName);

            List<RunData> dataList = new List<RunData>();

            IWorkbook book = null;
            ISheet sheet = null;

            using (FileStream FS = new FileStream(fileName, FileMode.Open, FileAccess.Read))
            {
                book = WorkbookFactory.Create(FS);
                sheet = book.GetSheetAt(0);

                for (int rowIndex = 8; rowIndex <= sheet.LastRowNum; rowIndex++)
                {
                    IRow row = sheet.GetRow(rowIndex);

                    //跑步结束时间 记录状态 悦跑号 用户昵称 性别 跑步距离（公里） 跑步耗时 跑步类型 平均配速（分钟/公里）
                    string[] values = ReadRowToArray(row, 11);

                    DateTime runEndTime = DateUtil.ParseDateTime(values[0]);
                    // values[1] ignored
                    long joyRunId = long.Parse(values[2]);
                    string name = values[3];
                    string gender = values[4];
                    double distance = float.Parse(values[5]);
                    double runTime = DateUtil.ParseTimeSpanToSeconds(values[6]);
                    string runType = values[7];
                    // values[8] re-calculate in constructor
                    int cadence = values[9] == "N/A" ? 0 : int.Parse(values[9]);
                    double strideLength = values[10] == "N/A" ? 0 : float.Parse(values[10]);

                    RunData runData = new RunData(joyRunId, name, gender, distance, runTime,
                        runType, runEndTime, cadence, strideLength);

                    if (checkDuplicate.ContainsKey(runData))
                    {
                        Logger.Info("Duplicate run data : {0}/{1}", runData.JoyRunId, runData.RunStartTime);
                    }
                    else
                    {
                        checkDuplicate.Add(runData, runData);
                        string sql = string.Format("INSERT INTO run_data VALUES({0}, '{1}', '{2}', '{3}', '{4}', {5}, {6},{7},{8},{9});",
                            runData.JoyRunId, runData.Name.Replace("'", "''"), runData.Gender,
                            runData.RunStartTime, runData.RunType,
                            runData.Distance, runData.TotalTimeSeconds, runData.AvgPaceSeconds,
                            runData.Cadence, runData.StrideLength);

                        sqls.Add(sql);
                    }
                }
            }
        }

        // 都以string读入是防止源头excel不按格式写数据，不管3721都先转string
        private static string[] ReadRowToArray(IRow row, int columnCount)
        {
            string[] values = new string[columnCount];
            for (int cellIndex = 0; cellIndex < values.Length; cellIndex++)
            {
                ICell cell = row.GetCell(cellIndex);
                string valueStr = string.Empty;
                switch (cell.CellType)
                {
                    case CellType.String:
                        valueStr = cell.StringCellValue;
                        break;
                    case CellType.Numeric:
                        valueStr = cell.NumericCellValue.ToString();
                        break;
                }
                values[cellIndex] = valueStr;
            }

            return values;
        }
    }
}
