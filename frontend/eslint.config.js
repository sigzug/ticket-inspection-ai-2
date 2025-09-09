import js from "@eslint/js";
import ts from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";

export default [
    {ignores: ["dist", "node_modules"]},
    js.configs.recommended,
    {
        files: ["**/*.ts", "**/*.tsx"],
        languageOptions: {parser: tsParser, parserOptions: {ecmaVersion: "latest", sourceType: "module"}},
        plugins: {"@typescript-eslint": ts},
        rules: {
            "no-unused-vars": "off",
            "@typescript-eslint/no-unused-vars": ["warn", {argsIgnorePattern: "^_", varsIgnorePattern: "^_"}],
            "no-console": ["warn", {allow: ["warn", "error"]}],
        },
    },
];
