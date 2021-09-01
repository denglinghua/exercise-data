using System.Data;
using System.Collections.Generic;

namespace RunData.DataAnalysis
{
    class SumGroup
    {
        public string Label { get; }
        public float Value { get; set; }
        public List<DataRow> DataRows { get; } = new List<DataRow>();
        public object MatchParam { get;}

        SumGroup(string label, object matchParam)
        {
            this.Label = label;
            this.MatchParam = matchParam;
        }

        SumGroup(GroupRange range) : this(range.Label, range)
        {
        }

        public void AddDataRow(DataRow dataRow)
        {
            this.DataRows.Add(dataRow);
        }

        public override string ToString()
        {
            return string.Format("{{{0}:{1}}}", this.Label, this.Value);
        }
    }
}
