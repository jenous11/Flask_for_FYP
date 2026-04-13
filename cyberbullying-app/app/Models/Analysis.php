<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Analysis extends Model
{
    protected $fillable = [
        'input_text',
        'label',
        'label_id',
        'confidence',
        'status',
    ];
}
