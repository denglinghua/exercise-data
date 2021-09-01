namespace RunData.DataAnalysis
{
    class GroupRange
    {
        public string Label { get; }
        public float Start { get; }
        public float End { get; }

        public GroupRange(string label, float start, float end)
        {
            this.Label = label;
            this.Start = start;
            this.End = end;
        }
    }
}
