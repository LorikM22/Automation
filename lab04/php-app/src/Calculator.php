<?php

declare(strict_types=1);

namespace App;

use InvalidArgumentException;

class Calculator
{
    public function add(float $a, float $b): float
    {
        return $a + $b;
    }

    public function subtract(float $a, float $b): float
    {
        return $a - $b;
    }

    public function multiply(float $a, float $b): float
    {
        return $a * $b;
    }

    public function divide(float $a, float $b): float
    {
        if ($b == 0.0) {
            throw new InvalidArgumentException('Împărțirea la zero nu este permisă.');
        }

        return $a / $b;
    }

    /**
     * Media aritmetică a unei liste de numere.
     *
     * @param float[] $numbers
     */
    public function average(array $numbers): float
    {
        if ($numbers === []) {
            throw new InvalidArgumentException('Lista de numere nu poate fi goală.');
        }

        return array_sum($numbers) / count($numbers);
    }
}
