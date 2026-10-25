<?php

declare(strict_types=1);

namespace Tests;

use App\Calculator;
use InvalidArgumentException;
use PHPUnit\Framework\TestCase;

class CalculatorTest extends TestCase
{
    private Calculator $calculator;

    protected function setUp(): void
    {
        $this->calculator = new Calculator();
    }

    public function testAdd(): void
    {
        $this->assertSame(5.0, $this->calculator->add(2, 3));
    }

    public function testSubtract(): void
    {
        $this->assertSame(-1.0, $this->calculator->subtract(2, 3));
    }

    public function testMultiply(): void
    {
        $this->assertSame(12.0, $this->calculator->multiply(3, 4));
    }

    public function testDivide(): void
    {
        $this->assertSame(2.5, $this->calculator->divide(5, 2));
    }

    public function testDivideByZeroThrowsException(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->calculator->divide(1, 0);
    }

    public function testAverage(): void
    {
        $this->assertSame(2.0, $this->calculator->average([1, 2, 3]));
    }

    public function testAverageOfEmptyListThrowsException(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->calculator->average([]);
    }
}
