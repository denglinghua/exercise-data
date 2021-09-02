using System;
using System.Collections.Generic;
using System.Data;

namespace RunData.DataAnalysis
{
    internal class Facade
    {
        public static void Analyze(DataSource dataSource)
        {
            DataTable sumData = AnalysisDataSource.CreateRunSumData(dataSource.RunRecords);
            DataTable detailData = AnalysisDataSource.CreateRunDetailData(dataSource.RunDetailRecords);

            List<GroupSet> detailGroupSets = new List<GroupSet>();
            detailGroupSets.Add(GroupSetRepo.CreateRunWeekDayGroupSet());
            detailGroupSets.Add(GroupSetRepo.CreateRunHourGroupSet());

            List<GroupSet> sumGroupSets = new List<GroupSet>();
            sumGroupSets.Add(GroupSetRepo.CreateRunCountGroupSet());
            sumGroupSets.Add(GroupSetRepo.CreateDistanceGroupSet());
            sumGroupSets.Add(GroupSetRepo.CreateAvgPaceGroupSet());
            sumGroupSets.Add(GroupSetRepo.CreateTotalTimeGroupSet());

            GroupSet.DoGroup(detailData, detailGroupSets);
            GroupSet.PrintGroupSets(detailGroupSets);

            GroupSet.DoGroup(sumData, sumGroupSets);
            GroupSet.PrintGroupSets(sumGroupSets);
        }
    }
}
