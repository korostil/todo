export const monthMap = [
  { shortName: "Jan", value: 1 },
  { shortName: "Feb", value: 2 },
  { shortName: "Mar", value: 3 },
  { shortName: "Apr", value: 4 },
  { shortName: "May", value: 5 },
  { shortName: "Jun", value: 6 },
  { shortName: "Jul", value: 7 },
  { shortName: "Aug", value: 8 },
  { shortName: "Sep", value: 9 },
  { shortName: "Oct", value: 10 },
  { shortName: "Nov", value: 11 },
  { shortName: "Dec", value: 12 },
];
export const monthShortNames = monthMap.map((item) => item.shortName);

export function getMonday(date) {
  let _date = new Date(date),
    day = _date.getDay(),
    diff = _date.getDate() - day + (day === 0 ? -6 : 1);
  return new Date(_date.setDate(diff));
}

export function getSunday(date) {
  let _date = new Date(date),
    day = _date.getDay(),
    diff = _date.getDate() + (day === 0 ? 0 : 7 - day);
  return new Date(_date.setDate(diff));
}

export function toUnixDate(date) {
  if (date) {
    return date.toISOString().split("T")[0];
  }
  return null;
}

export function getStartOfTheDay(date) {
  let _date = new Date(date);
  _date.setHours(Math.abs(date.getTimezoneOffset()) / 60, 0, 0, 0);
  return _date;
}

export function getFormattedDueDateTime(due_date, due_time) {
  let result = null;

  if (due_date !== null) {
    due_date = new Date(due_date);
    result = due_date.getDate() + " " + monthShortNames[due_date.getMonth()];
    let year = due_date.getFullYear();

    if (new Date().getFullYear() !== year)
      result += " " + due_date.getFullYear();
  }

  if (due_time !== null) {
    due_time = due_time.slice(0, -3);
    if (result) result += " " + due_time;
    else result = due_time;
  }

  return result;
}
