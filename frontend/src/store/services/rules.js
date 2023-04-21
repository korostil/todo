import { getStartOfTheDay } from "@/store/services/utils/dates";

export const titleRules = [
  (value) => {
    if (value) return true;

    return "Title is required.";
  },
  (value) => {
    if (value?.length <= 128) return true;

    return "Title must be less than 128 characters.";
  },
];
export const descriptionRules = [
  (value) => {
    if (value) return true;

    return "Description is required.";
  },
  (value) => {
    if (value?.length <= 128) return true;

    return "Description must be less than 128 characters.";
  },
];

export const taskDueDateRules = [
  (value) => {
    if (new Date(value) >= getStartOfTheDay(new Date())) return true;

    return "Date must be greater than today";
  },
];
