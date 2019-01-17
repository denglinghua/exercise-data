using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

using NPOI.HSSF.UserModel;
using NPOI.SS.UserModel;
using NPOI.SS.Util;

namespace RunData
{
    class DataSource
    {
        public DateRange CurrentDateRange;
        public string Group;
        public List<RunRecord> RunRecoreds;
        public NoRunData NoRunData;
        public NonBreakRunData NonBreakRunData;
        private List<long> LeaveMemberIdList;        

        public static readonly DataSource Instance = new DataSource();

        public static readonly string NO_RUN_DATA_FILE = "no_run_data.txt";
        public static readonly string NON_BREAK_RUN_DATA_FILE = "no_break_run_data.txt";        

        public static void Init(string runRecordFile, string[] noRunFiles, string leaveFile)
        {
            Instance.LoadRunRecord(runRecordFile);

            Instance.LoadNoRunData(noRunFiles);

            Instance.LoadLeaveData(leaveFile);

            Instance.LoadPreviousNoRunData(NO_RUN_DATA_FILE);

            Instance.LoadPreviousNonBreakRunData(NON_BREAK_RUN_DATA_FILE);
        }

        public void HandleData()
        {
            this.ClassifyRunData();

            this.NoRunData.HandleData(this.LeaveMemberIdList);

            this.NonBreakRunData.HandleData();
        }

        private void ClassifyRunData()
        {
            Logger.Info("开始分离跑步达标和不达标的数据...");

            foreach (RunRecord r in this.RunRecoreds)
            {
                string reason = null;

                if (!r.IsQualifiedOfDistance)
                {
                    reason = string.Format("跑量：{0}", r.Distance);
                }

                if (!r.IsQualifiedOfAvgPace)
                {
                    reason = string.Format("配速：{0}", RunRecord.ToTimeSpanFromSeconds(r.AvgPaceSeconds));
                }


                if (reason != null)
                {
                    this.NoRunData.AddCurrentNoRunRecord(r.Member, reason, CurrentDateRange);
                }
                else
                {
                    this.NonBreakRunData.AddCurrentNoRunRecord(r.Member, CurrentDateRange);
                }
            }
        }

        private void LoadRunRecord(string fileName)
        {
            Logger.Info("开始加载跑步统计数据...");

            IWorkbook book = null;
            ISheet sheet = null;

            using (FileStream FS = new FileStream(fileName, FileMode.Open, FileAccess.Read))
            {
                book = WorkbookFactory.Create(FS);
                sheet = book.GetSheetAt(0);

                this.Group = GetCellByReference(sheet, "B1").StringCellValue;

                ICell dataRangeCell = GetCellByReference(sheet, "B3");
                String dataRangeStr = dataRangeCell.StringCellValue;
                this.CurrentDateRange = DateRange.Create(dataRangeStr.Split(new String[] { "--" }, StringSplitOptions.None), "yyyy-MM-dd HH:mm:ss");

                this.RunRecoreds = new List<RunRecord>();
                for (int rowIndex = 10; rowIndex <= sheet.LastRowNum; rowIndex++)
                {
                    IRow row = sheet.GetRow(rowIndex);

                    //用户昵称  用户ID  所属跑团名称  性别  总跑量（公里）  总用时  跑步次数
                    string[] values = ReadRowToArray(row, 7);

                    this.RunRecoreds.Add(
                        new RunRecord(long.Parse(values[1]), values[0], values[3], values[2], float.Parse(values[4]), TimeSpan.Parse(values[5]).TotalSeconds,
                        short.Parse(values[6])));
                }
            }
        }

        private void LoadNoRunData(string[] noRunFiles)
        {
            Logger.Info("开始加载无跑步成员数据...");

            this.NoRunData = new NoRunData();
            foreach (string fileName in noRunFiles)
            {
                LoadOneFileNoRunMembers(fileName);
            }
        }

        private void LoadOneFileNoRunMembers(string fileName)
        {
            IWorkbook book = null;
            ISheet sheet = null;

            using (FileStream FS = new FileStream(fileName, FileMode.Open, FileAccess.Read))
            {
                book = WorkbookFactory.Create(FS);
                sheet = book.GetSheetAt(0);

                ICell groupCell = GetCellByReference(sheet, "B4");
                String groupName = groupCell.StringCellValue;

                for (int rowIndex = 6; rowIndex <= sheet.LastRowNum; rowIndex++)
                {
                    IRow row = sheet.GetRow(rowIndex);

                    //悦跑ID 昵称 性别 总跑量（公里） 最后跑步时间
                    string[] values = ReadRowToArray(row, 3);

                    this.NoRunData.AddCurrentNoRunRecord(new Member(long.Parse(values[0]), values[1], values[2], groupName), "没跑步", CurrentDateRange);
                }
            }
        }

        private void LoadLeaveData(string fileName)
        {
            Logger.Info("开始加载请假数据...");

            IWorkbook book = null;
            ISheet sheet = null;

            using (FileStream FS = new FileStream(fileName, FileMode.Open, FileAccess.Read))
            {
                book = WorkbookFactory.Create(FS);
                sheet = book.GetSheetAt(0);

                this.LeaveMemberIdList = new List<long>();
                for (int rowIndex = 3; rowIndex <= sheet.LastRowNum; rowIndex++)
                {
                    IRow row = sheet.GetRow(rowIndex);

                    //报名时间 昵称 悦跑圈ID号  请假原因
                    string[] values = ReadRowToArray(row, 4);

                    this.LeaveMemberIdList.Add(long.Parse(values[2]));
                }
            }
        }

        private void LoadPreviousNoRunData(string fileName)
        {
            if (!File.Exists(fileName))
            {
                return;
            }

            Logger.Info("开始加载过往连续不达标数据...");

            string[] lines = File.ReadAllLines(fileName);
            foreach (string s in lines)
            {
                //88474417	Samryi	男	广·马帮_神马分队	20190107-20190113
                string[] a = s.Split('\t');
                this.NoRunData.AddPreviousNoRunRecord(new Member(long.Parse(a[0]), a[1], a[2], a[3]),
                    a[4].Split(','));
            }
        }

        private void LoadPreviousNonBreakRunData(string fileName)
        {
            if (!File.Exists(fileName))
            {
                return;
            }

            Logger.Info("开始加载过去连续达标数据...");

            this.NonBreakRunData = new NonBreakRunData();

            string[] lines = File.ReadAllLines(fileName);
            foreach (string s in lines)
            {
                //88474417	Samryi	男	广·马帮_神马分队	20190107-20190113
                string[] a = s.Split('\t');
                this.NonBreakRunData.AddPreviousRunRecord(new Member(long.Parse(a[0]), a[1], a[2], a[3]),
                    a[4].Split(','));
            }
        }

        private static ICell GetCellByReference(ISheet sheet, string reference)
        {
            CellReference cr = new CellReference(reference);
            IRow row = sheet.GetRow(cr.Row);
            return row.GetCell(cr.Col);
        }

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
