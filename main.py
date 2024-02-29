# Функции
from Core.everything_load import final_everything_load_test_case
from Core.vacancy_export import ai_parse_description
from Core.resume_export import ai_parse_about
from Core.matching_thingy import match_strings


def add_dict_to_dict(main_dict, key, value_dict):
    main_dict[key] = value_dict


score_table = {}


def main():
    everything_loaded = final_everything_load_test_case()
    for i in range(len(everything_loaded)):
        resumes = everything_loaded[i][1]
        score_table[i] = {}
        print(everything_loaded[i][0][1])
        print(ai_parse_about(everything_loaded[i][0][2]))
        if everything_loaded[i][0][1] is None:
            string_2 = ai_parse_about(everything_loaded[i][0][2])
        else:
            string_2 = everything_loaded[i][0][1] + ai_parse_about(everything_loaded[i][0][2])
        for j in range(len(resumes)):
            string_1 = ai_parse_description(resumes[1] + resumes[4][0])
            result = match_strings(string_1, string_2)
            local_score = result * 10 + resumes[4][1] * 3 + resumes[5][1] * 1
            score_table[i][j] = local_score

    print(score_table)


# Run the main function
if __name__ == "__main__":
    main()
