using System;
using System.Collections.Generic;
using System.Data;

namespace RunData.DataAnalysis
{
    internal class Facade
    {
        public void Analyze(List<PeriodRunRecord> sumRunData, List<RunRecordDetail> detailRunData)
        {
            DataTable sumData = AnalysisDataSource.CreateRunSumData(sumRunData);
            DataTable deitalData = AnalysisDataSource.CreateRunDetailData(detailRunData);
        }
    }
}
