using System;

namespace RunData
{
    class Member
    {
        public long JoyRunId { get; }
        public string Name { get; }
        public string Gender { get; }
        public DateTime JoinDate { get; set; }
        public bool IsActive = false;

        public Group Group;

        public Member(long joyRunId, string name, string gender, string groupName)
        {
            this.JoyRunId = joyRunId;
            this.Name = name;
            this.Gender = gender;
            this.Group = Group.GetByName(groupName);
        }        

        public override bool Equals(object obj)
        {
            return this.JoyRunId == ((Member)obj).JoyRunId;
        }

        public override int GetHashCode()
        {
            return this.JoyRunId.GetHashCode();
        }

        public override string ToString()
        {
            return string.Format("{0}\t{1}\t{2}\t{3}", this.JoyRunId, this.Name, this.Gender, this.Group.ShortName);
        }

        public static Member Create(string[] a)
        {
            return new Member(long.Parse(a[0]), a[1], a[2], a[3]);
        }
    }
}
