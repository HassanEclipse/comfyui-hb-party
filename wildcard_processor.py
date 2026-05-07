#JN_Wildcard Processor v1.5 (sub folders)
import os
import re
import random
import folder_paths

class HB_WildcardProcessor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "This is another __places__ with a __colors__ chair.", "multiline": True}),
                "seed": ("INT", {"default": 42}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)  # Add report string as second output
    RETURN_NAMES = ("text", "report",)
    FUNCTION = "process"
    CATEGORY = "JN_Party"

    def process(self, text, seed):
        rnd = random.Random(seed)
        self.report_data = {}  # key: wildcard name, value: extracted [title]
        text = self._process_bracket_wildcards(text, rnd)
        text = self._process_advanced_file_wildcards(text, seed)
        report_string = self._format_report()
        return (text, report_string)

    def _format_report(self):
        lines = []
        for k, v in self.report_data.items():
            lines.append(f"[{k.capitalize()}]: {v}")
        return "\n".join(lines)

    def _process_bracket_wildcards(self, text, rnd):
        pattern = re.compile(r'\{([^{}]*)\}')

        def parse_options(option_text):
            parts = option_text.split('|')
            options = []
            weights = []
            for part in parts:
                match = re.match(r'(\d+)::(.*)', part)  # ← no strip!
                if match:
                    weights.append(int(match.group(1)))
                    options.append(match.group(2))
                else:
                    weights.append(1)
                    options.append(part.strip())
            return options, weights

        def replace(match):
            inner = match.group(1)
            # Recursively process nested brackets inside options before choosing
            options, weights = parse_options(inner)
            resolved_options = [self._process_bracket_wildcards(opt, rnd) for opt in options]
            return rnd.choices(resolved_options, weights)[0]

        # Keep evaluating while any {...} remains
        while pattern.search(text):
            text = pattern.sub(replace, text)

        return text


    def _process_advanced_file_wildcards(self, prompt, seed, debug=False):
        wildcard_path = os.path.join(folder_paths.get_user_directory(), 'wildcards')
        if not os.path.isdir(wildcard_path):
            wildcard_path = os.path.join(os.path.dirname(folder_paths.__file__), 'wildcards')

        wildcard_regex = r'((\d+)\$\$)?__(!|\+|-|\*)?([a-zA-Z0-9_/]+)((?:\|[^|]+)*)__'

        match_strings = []
        random.seed(seed)
        offset = seed
        new_prompt = ''
        last_end = 0

        for m in re.finditer(wildcard_regex, prompt):
            full_match = m.group(0)
            lines_count_str = m.group(2)
            offset_type = m.group(3)
            actual_match = m.group(4)
            words_to_find_str = m.group(5)

            new_prompt += prompt[last_end:m.start()]

            wildcard_key = actual_match.replace("_", " ").strip()

            lock_indicator = offset_type == '!'
            increment_indicator = offset_type == '+'
            decrement_indicator = offset_type == '-'
            random_indicator = offset_type == '*'

            words_to_find = words_to_find_str.split('|')[1:] if words_to_find_str else None
            lines_to_insert = int(lines_count_str) if lines_count_str else 1

            match_parts = actual_match.split('/')
            if len(match_parts) > 1:
                wildcard_dir = os.path.join(*match_parts[:-1])
                wildcard_file = match_parts[-1]
            else:
                wildcard_dir = ''
                wildcard_file = match_parts[0]

            search_path = os.path.join(wildcard_path, wildcard_dir)
            file_path = os.path.join(search_path, wildcard_file + '.txt')

            if not os.path.isfile(file_path) and wildcard_dir == '':
                file_path = os.path.join(wildcard_path, wildcard_file + '.txt')

            if os.path.isfile(file_path):
                store_offset = None
                if actual_match in match_strings:
                    store_offset = offset
                    if lock_indicator:
                        offset = seed
                    elif random_indicator:
                        offset = random.randint(0, 1000000)
                    elif increment_indicator:
                        offset = seed + 1
                    elif decrement_indicator:
                        offset = seed - 1
                    else:
                        offset = random.randint(0, 1000000)

                selected_lines = []
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_lines = [line.strip() for line in file if line.strip()]
                    num_lines = len(file_lines)

                    if words_to_find:
                        for i in range(lines_to_insert):
                            start_idx = (offset + i) % num_lines
                            for j in range(num_lines):
                                line_number = (start_idx + j) % num_lines
                                line = file_lines[line_number]
                                if any(re.search(r'\b' + re.escape(word) + r'\b', line, re.IGNORECASE) for word in words_to_find):
                                    selected_lines.append(line)
                                    break
                    else:
                        start_idx = offset % num_lines
                        for i in range(lines_to_insert):
                            line_number = (start_idx + i) % num_lines
                            selected_lines.append(file_lines[line_number])

                # Clean lines and extract [Title]s for report
                replacements = []
                for line in selected_lines:
                    title_match = re.match(r'\[([^\[\]]+)\]\s*(.+)', line)
                    if title_match:
                        title, content = title_match.groups()
                        replacements.append(content.strip())
                        self.report_data[wildcard_file] = title.strip()
                    else:
                        replacements.append(line.strip())

                replacement_text = ', '.join(replacements)
                new_prompt += replacement_text
                match_strings.append(actual_match)

                if store_offset is not None:
                    offset = store_offset
                    store_offset = None
                offset += lines_to_insert
            else:
                new_prompt += full_match  # leave as-is if not found

            last_end = m.end()

        new_prompt += prompt[last_end:]
        return new_prompt
