import { MapPin, Briefcase } from 'lucide-react';
import { cn } from '../lib/utils';

interface FiltersProps {
  jurisdiction: string;
  onJurisdictionChange: (value: string) => void;
  practiceArea: string;
  onPracticeAreaChange: (value: string) => void;
  disabled?: boolean;
}

const jurisdictions = [
  { value: 'US', label: 'United States' },
  { value: 'CA', label: 'Canada' },
  { value: 'UK', label: 'United Kingdom' },
  { value: 'AU', label: 'Australia' },
  { value: 'INTL', label: 'International' },
];

const practiceAreas = [
  { value: 'general', label: 'General' },
  { value: 'contract', label: 'Contract Law' },
  { value: 'criminal', label: 'Criminal Law' },
  { value: 'family', label: 'Family Law' },
  { value: 'employment', label: 'Employment Law' },
  { value: 'corporate', label: 'Corporate Law' },
  { value: 'intellectual', label: 'Intellectual Property' },
];

export function Filters({
  jurisdiction,
  onJurisdictionChange,
  practiceArea,
  onPracticeAreaChange,
  disabled = false,
}: FiltersProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      {/* Jurisdiction Filter */}
      <div className="space-y-2">
        <label className="flex items-center gap-2 text-sm font-semibold text-foreground">
          <MapPin className="w-4 h-4 text-primary" />
          Jurisdiction
        </label>
        <select
          value={jurisdiction}
          onChange={(e) => onJurisdictionChange(e.target.value)}
          disabled={disabled}
          className={cn(
            "w-full px-3 py-2 rounded-lg border border-border bg-background text-foreground",
            "focus:outline-none focus:ring-2 focus:ring-primary",
            "transition-all duration-200",
            disabled && "opacity-50 cursor-not-allowed"
          )}
        >
          {jurisdictions.map((j) => (
            <option key={j.value} value={j.value}>
              {j.label}
            </option>
          ))}
        </select>
      </div>

      {/* Practice Area Filter */}
      <div className="space-y-2">
        <label className="flex items-center gap-2 text-sm font-semibold text-foreground">
          <Briefcase className="w-4 h-4 text-primary" />
          Practice Area
        </label>
        <select
          value={practiceArea}
          onChange={(e) => onPracticeAreaChange(e.target.value)}
          disabled={disabled}
          className={cn(
            "w-full px-3 py-2 rounded-lg border border-border bg-background text-foreground",
            "focus:outline-none focus:ring-2 focus:ring-primary",
            "transition-all duration-200",
            disabled && "opacity-50 cursor-not-allowed"
          )}
        >
          {practiceAreas.map((p) => (
            <option key={p.value} value={p.value}>
              {p.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
