<?php

declare(strict_types=1);

namespace App;

class StringHelper
{
    /**
     * Transformă un text într-un "slug" pentru URL: "Salut Lume!" -> "salut-lume".
     */
    public function slugify(string $text): string
    {
        $text = mb_strtolower(trim($text));
        $text = preg_replace('/[^a-z0-9]+/u', '-', $text) ?? '';

        return trim($text, '-');
    }

    public function isPalindrome(string $text): bool
    {
        $clean = preg_replace('/[^a-z0-9]/', '', strtolower($text)) ?? '';

        return $clean === strrev($clean);
    }

    public function wordCount(string $text): int
    {
        $text = trim($text);

        return $text === '' ? 0 : count(preg_split('/\s+/', $text) ?: []);
    }
}
