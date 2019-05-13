using System;
using System.Collections.Generic;
using System.Text;

namespace RunData
{
    class Group
    {
        private static readonly string[] ShortNames;
        private static readonly Dictionary<string, Group> Groups = new Dictionary<string, Group>();

        public string Name { get; }
        public string ShortName { get; }
        public bool Disabled { get; }

        static Group()
        {
            var setting = Properties.Settings.Default.GroupShortNames;
            ShortNames = new string[setting.Count];
            setting.CopyTo(ShortNames, 0);
        }

        public static Group GetByName(string name)
        {
            Group g;
            if (!Groups.TryGetValue(name, out g))
            {
                g = new Group(name);
                Groups[name] = g;
            }
            return g;
        }

        private Group(string name)
        {
            this.Name = name;
            this.ShortName = this.Name;
            this.Disabled = true;

            foreach (string shortName in ShortNames)
            {
                if (name.Contains(shortName))
                {
                    this.Disabled = false;
                    this.ShortName = shortName;
                    break;
                }
            }
        }

        public override bool Equals(object obj)
        {
            return this.Name.Equals(((Group)obj).Name);
        }

        public override int GetHashCode()
        {
            return this.Name.GetHashCode();
        }
    }
}
