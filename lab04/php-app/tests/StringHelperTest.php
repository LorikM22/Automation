<?php

declare(strict_types=1);

namespace Tests;

use App\StringHelper;
use PHPUnit\Framework\TestCase;

class StringHelperTest extends TestCase
{
    private StringHelper $helper;

    protected function setUp(): void
    {
        $this->helper = new StringHelper();
    }

    public function testSlugify(): void
    {
        $this->assertSame('salut-lume', $this->helper->slugify('  Salut Lume!  '));
        $this->assertSame('jenkins-ci-cd-2026', $this->helper->slugify('Jenkins CI/CD 2026'));
    }

    public function testIsPalindrome(): void
    {
        $this->assertTrue($this->helper->isPalindrome('Ele fac cafele'));
        $this->assertFalse($this->helper->isPalindrome('Jenkins'));
    }

    public function testWordCount(): void
    {
        $this->assertSame(3, $this->helper->wordCount('unu  doi trei'));
        $this->assertSame(0, $this->helper->wordCount('   '));
    }
}
