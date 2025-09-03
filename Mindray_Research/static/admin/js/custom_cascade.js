console.log('=== Brand-Model Cascade Script Loading ===');

(function() {
    'use strict';
    
    var $ = window.$ || window.django.jQuery;
    
    function initCascade() {
        console.log('=== Initializing Brand-Model Cascade ===');
        
        // 查找所有brand选择器（包括inline中的）
        var brandSelectors = 'select[name="brand"], select[name*="-brand"]';
        var $brandSelects = $(brandSelectors);
        
        console.log('Found brand selects:', $brandSelects.length);
        
        $brandSelects.each(function(index) {
            var $brandSelect = $(this);
            var brandName = $brandSelect.attr('name') || $brandSelect.attr('id') || '';
            
            console.log('Processing brand select:', index, brandName);
            
            // 避免重复绑定
            if ($brandSelect.data('cascade-bound')) {
                console.log('Already bound, skipping...');
                return;
            }
            
            $brandSelect.data('cascade-bound', true);
            
            // 移除旧的事件处理器
            $brandSelect.off('change.cascade');
            
            // 绑定新的事件处理器
            $brandSelect.on('change.cascade', function() {
                console.log('🔥 Brand changed:', this.name, 'value:', this.value);
                handleBrandChange($(this), false); // false表示不是初始加载
            });
            
            // 🔑 关键修改：页面初始加载时，如果brand有值但model选项很少，才重新加载model
            var $modelSelect = findModelSelect($brandSelect);
            if ($modelSelect && $modelSelect.length > 0 && $brandSelect.val()) {
                var currentModelOptions = $modelSelect.find('option').length;
                console.log('Current model options count:', currentModelOptions);
                
                // 只有当model选项很少时（比如只有默认的"---"选项）才重新加载
                if (currentModelOptions <= 1) {
                    console.log('Model options insufficient, loading for brand:', $brandSelect.val());
                    handleBrandChange($brandSelect, true); // true表示是初始加载
                }
            }
            
            console.log('✅ Event bound for:', brandName);
        });
    }
    
    function handleBrandChange($brandSelect, isInitialLoad) {
        var brandId = $brandSelect.val();
        var $modelSelect = findModelSelect($brandSelect);
        
        if (!$modelSelect || $modelSelect.length === 0) {
            console.error('❌ Model select not found for brand:', $brandSelect.attr('name'));
            return;
        }
        
        console.log('✅ Found model select:', $modelSelect.attr('name'));
        
        // 🔑 关键修改：保存当前选中的model值
        var currentModelValue = $modelSelect.val();
        console.log('Current model value:', currentModelValue);
        
        if (brandId && brandId !== '') {
            console.log('Loading models for brand ID:', brandId);
            loadModels($modelSelect, brandId, currentModelValue, isInitialLoad);
        } else {
            console.log('Clearing models');
            clearModels($modelSelect);
        }
    }
    
    function findModelSelect($brandSelect) {
        var brandName = $brandSelect.attr('name') || '';
        var brandId = $brandSelect.attr('id') || '';
        
        console.log('Finding model select for:', brandName, brandId);
        
        // 方法1：基于name属性模式匹配
        if (brandName) {
            var modelName = brandName.replace('brand', 'model');
            console.log('Looking for model name:', modelName);
            
            var $modelSelect = $('select[name="' + modelName + '"]');
            if ($modelSelect.length > 0) {
                console.log('✅ Found by name pattern');
                return $modelSelect;
            }
        }
        
        // 方法2：基于id属性模式匹配
        if (brandId) {
            var modelId = brandId.replace('brand', 'model');
            console.log('Looking for model id:', modelId);
            
            var $modelSelect = $('#' + modelId);
            if ($modelSelect.length > 0) {
                console.log('✅ Found by id pattern');
                return $modelSelect;
            }
        }
        
        // 方法3：在同一个容器中查找
        var $container = $brandSelect.closest('tr, .form-row, .field-box, .inline-related, .tabular, .stacked');
        if ($container.length > 0) {
            console.log('Searching in container...');
            
            var $modelSelects = $container.find('select[name*="model"]');
            console.log('Found model selects in container:', $modelSelects.length);
            
            if ($modelSelects.length > 0) {
                console.log('✅ Found in container');
                return $modelSelects.first();
            }
        }
        
        console.log('❌ Model select not found');
        return $();
    }
    
    function loadModels($modelSelect, brandId, currentModelValue, isInitialLoad) {
        // 🔑 关键修改：如果是初始加载且已经有足够的选项，可能不需要重新加载
        if (isInitialLoad && $modelSelect.find('option').length > 2) {
            console.log('Initial load: model already has options, keeping current selection');
            return;
        }
        
        // 显示loading状态
        $modelSelect.html('<option value="">Loading...</option>');
        
        // AJAX请求
        $.ajax({
            url: '/admin/get_models_by_brand/',
            method: 'GET',
            data: { brand_id: brandId },
            success: function(data) {
                console.log('✅ Models loaded:', data.length);
                updateModels($modelSelect, data, currentModelValue);
            },
            error: function(xhr, status, error) {
                console.error('❌ Error loading models:', error);
                $modelSelect.html('<option value="">Error loading models</option>');
            }
        });
    }
    
    function updateModels($modelSelect, models, previousValue) {
        $modelSelect.html('<option value="">---------</option>');
        
        var foundPreviousValue = false;
        
        $.each(models, function(i, model) {
            var $option = $('<option></option>').val(model.id).text(model.name);
            $modelSelect.append($option);
            
            // 检查是否找到了之前的选中值
            if (previousValue && model.id == previousValue) {
                foundPreviousValue = true;
            }
        });
        
        // 🔑 关键修改：尝试恢复之前的选中值
        if (previousValue && foundPreviousValue) {
            $modelSelect.val(previousValue);
            console.log('✅ Restored previous model value:', previousValue);
        } else if (previousValue) {
            console.log('⚠️ Previous model value not found in new options:', previousValue);
        }
        
        console.log('✅ Model options updated');
    }
    
    function clearModels($modelSelect) {
        $modelSelect.html('<option value="">---------</option>');
    }
    
    // 设置事件监听器来处理动态添加的inline表单
    function setupEventListeners() {
        console.log('Setting up event listeners...');
        
        // 监听点击"Add another"按钮
        $(document).on('click', '.add-row a, .addlink', function(e) {
            console.log('🔥 Add another clicked!');
            
            // 延迟重新初始化
            setTimeout(function() {
                console.log('Re-initializing cascade...');
                initCascade();
            }, 500);
            
            setTimeout(function() {
                console.log('Second re-initialization...');
                initCascade();
            }, 1500);
        });
        
        // 监听DOM变化（备用方案）
        if (window.MutationObserver) {
            var observer = new MutationObserver(function(mutations) {
                var shouldReinit = false;
                
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'childList') {
                        $(mutation.addedNodes).each(function() {
                            if (this.nodeType === 1 && $(this).find('select[name*="brand"]').length > 0) {
                                console.log('🔥 New brand select detected via mutation observer');
                                shouldReinit = true;
                            }
                        });
                    }
                });
                
                if (shouldReinit) {
                    setTimeout(initCascade, 300);
                    setTimeout(initCascade, 1000);
                }
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
    }
    
    // 初始化函数
    function initialize() {
        console.log('🚀 Starting cascade initialization...');
        
        // 等待DOM完全加载
        $(document).ready(function() {
            console.log('DOM ready, initializing...');
            
            initCascade();
            setupEventListeners();
            
            // 延迟再次初始化，但要更保守
            setTimeout(function() {
                // 只初始化那些没有bound标记的新字段
                var $unboundBrands = $('select[name*="brand"]:not([data-cascade-bound="true"])');
                if ($unboundBrands.length > 0) {
                    console.log('Found unbound brand selects, initializing...');
                    initCascade();
                }
            }, 1000);
        });
    }
    
    // 启动
    initialize();
    
    // 导出调试函数到全局作用域
    window.debugCascade = function() {
        console.log('=== Cascade Debug Info ===');
        console.log('jQuery available:', typeof $ !== 'undefined');
        console.log('Brand selects found:', $('select[name*="brand"]').length);
        console.log('Model selects found:', $('select[name*="model"]').length);
        console.log('Bound brand selects:', $('select[name*="brand"][data-cascade-bound="true"]').length);
        
        $('select[name*="brand"]').each(function(i) {
            var $brandSelect = $(this);
            var $modelSelect = findModelSelect($brandSelect);
            console.log('Brand select', i, ':', 
                       $brandSelect.attr('name'), 
                       'value:', $brandSelect.val(),
                       'bound:', $brandSelect.data('cascade-bound'),
                       'model value:', $modelSelect.length > 0 ? $modelSelect.val() : 'not found');
        });
    };
    
})();

console.log('=== Brand-Model Cascade Script Loaded ===');