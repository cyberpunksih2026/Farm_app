import Fuse from 'fuse.js';

export const PRODUCTS = [
  {
    id: 'prod-tomato-hybrid',
    slug: 'fresh-farm-tomatoes',
    name: 'Red Vine Farm Tomatoes',
    categorySlug: 'vegetables',
    categoryName: 'Vegetables',
    price: 34,
    farmerPrice: 27,
    marketPrice: 45,
    unit: '1 kg',
    image: 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=800&q=80',
    fpoName: 'Sahyadri Farmer Producer Co.',
    fpoLocation: 'Nashik, Maharashtra',
    farmerLead: 'Ramesh Patil',
    freshnessTag: 'Harvested Today 5:00 AM',
    rating: 4.8,
    ratingCount: 142,
    inStock: true,
    stockKg: 450,
    organicCertified: true,
    description: 'Juicy, naturally vine-ripened farm tomatoes picked at daybreak. Free from synthetic growth regulators and wax coating.',
    highlights: ['Zero chemical ripening', 'Packed in breathable kraft baskets', 'Directly dispatched within 6 hours of harvest'],
    nutrition: { calories: '18 kcal', carbs: '3.9g', vitaminC: '28% RDA', potassium: '237mg' },
    shelfLife: '5-7 days in cool storage'
  },
  {
    id: 'prod-shimla-capsicum',
    slug: 'crisp-green-capsicum',
    name: 'Crisp Green Bell Pepper (Capsicum)',
    categorySlug: 'vegetables',
    categoryName: 'Vegetables',
    price: 48,
    farmerPrice: 38,
    marketPrice: 65,
    unit: '500 g',
    image: 'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?auto=format&fit=crop&w=800&q=80',
    fpoName: 'Shivalik Valley Growers FPO',
    fpoLocation: 'Solan, Himachal Pradesh',
    farmerLead: 'Virender Thakur',
    freshnessTag: 'Cold-chain Arrived',
    rating: 4.7,
    ratingCount: 89,
    inStock: true,
    stockKg: 280,
    organicCertified: false,
    description: 'Thick-walled, crisp green capsicums grown in polyhouse micro-climates for uniform crunch and high vitamin density.',
    highlights: ['Polyhouse greenhouse grown', 'High moisture retention', 'Grade A export quality sort'],
    nutrition: { calories: '20 kcal', carbs: '4.6g', vitaminC: '134% RDA', potassium: '175mg' },
    shelfLife: '7-10 days refrigerated'
  },
  {
    id: 'prod-baby-spinach',
    slug: 'tender-baby-spinach',
    name: 'Tender Hydroponic Baby Spinach (Palak)',
    categorySlug: 'leafy-greens',
    categoryName: 'Leafy Greens',
    price: 28,
    farmerPrice: 22,
    marketPrice: 40,
    unit: '250 g pack',
    image: 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?auto=format&fit=crop&w=800&q=80',
    fpoName: 'GreenRoots Agri Collective',
    fpoLocation: 'Pune Outskirts, Maharashtra',
    farmerLead: 'Sunita Deshmukh',
    freshnessTag: 'Harvested 3 Hours Ago',
    rating: 4.9,
    ratingCount: 210,
    inStock: true,
    stockKg: 120,
    organicCertified: true,
    description: 'Tender baby spinach leaves hydro-washed with pure ozone water. 100% soil-residue free and ready to cook or blend in smoothies.',
    highlights: ['Ozone triple-washed', 'Zero grit or mud residue', 'High bioavailable iron & folates'],
    nutrition: { calories: '23 kcal', carbs: '3.6g', iron: '2.7mg', vitaminA: '188% RDA' },
    shelfLife: '4-5 days crisp seal'
  },
  {
    id: 'prod-alphonso-mango',
    slug: 'ratnagiri-alphonso-mangoes',
    name: 'Original Ratnagiri Alphonso Mangoes (Hapus)',
    categorySlug: 'fruits',
    categoryName: 'Fresh Fruits',
    price: 680,
    farmerPrice: 560,
    marketPrice: 850,
    unit: '1 Dozen (12 pcs)',
    image: 'https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=800&q=80',
    fpoName: 'Konkan Mango Growers Cooperative',
    fpoLocation: 'Devgad, Ratnagiri, Maharashtra',
    farmerLead: 'Anant Gawade',
    freshnessTag: 'Naturally Hay Ripened',
    rating: 4.95,
    ratingCount: 312,
    inStock: true,
    stockKg: 180,
    organicCertified: true,
    description: 'GI-tagged authentic Ratnagiri Alphonso mangoes. Tree-matured and traditionally straw-ripened without harmful calcium carbide chemicals.',
    highlights: ['GI Tag Certified Devgad/Ratnagiri', 'Zero carbide ripening', 'Unbeatable saffron aroma and rich saffron pulp'],
    nutrition: { calories: '60 kcal', sugars: '13.7g', vitaminC: '60% RDA', vitaminA: '21% RDA' },
    shelfLife: '5-8 days at room temp'
  },
  {
    id: 'prod-kashmiri-apples',
    slug: 'kashmiri-royal-delicious-apples',
    name: 'Kashmiri Royal Delicious Apples',
    categorySlug: 'fruits',
    categoryName: 'Fresh Fruits',
    price: 165,
    farmerPrice: 130,
    marketPrice: 220,
    unit: '1 kg (4-5 pcs)',
    image: 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=800&q=80',
    fpoName: 'Shopian Orchardist Producer Society',
    fpoLocation: 'Shopian, Jammu & Kashmir',
    farmerLead: 'Bashir Ahmed Mir',
    freshnessTag: 'Direct Cold Air Freight',
    rating: 4.85,
    ratingCount: 178,
    inStock: true,
    stockKg: 350,
    organicCertified: false,
    description: 'Sweet, aromatic crisp red apples grown on pristine high-altitude Himalayan slopes. Naturally un-waxed skin.',
    highlights: ['High altitude orchard yield', '100% natural peel, zero wax polishing', 'Sweet balanced acidity with crisp bite'],
    nutrition: { calories: '52 kcal', dietaryFiber: '2.4g', vitaminC: '14% RDA', potassium: '107mg' },
    shelfLife: '14-20 days refrigerated'
  },
  {
    id: 'prod-red-onions',
    slug: 'lasalgaon-red-onions',
    name: 'Lasalgaon Premium Red Onions',
    categorySlug: 'vegetables',
    categoryName: 'Vegetables',
    price: 32,
    farmerPrice: 25,
    marketPrice: 42,
    unit: '1 kg',
    image: 'https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?auto=format&fit=crop&w=800&q=80',
    fpoName: 'Godavari Agri Farmer Producer Co.',
    fpoLocation: 'Lasalgaon, Nashik, Maharashtra',
    farmerLead: 'Kishore Bhamare',
    freshnessTag: 'Naturally Cured',
    rating: 4.7,
    ratingCount: 164,
    inStock: true,
    stockKg: 1200,
    organicCertified: false,
    description: 'Pungent, firm-layered pinkish-red onions cured in ventilated solar sheds for maximum storage life and aromatic cooking base.',
    highlights: ['Medium-pungency high sulfur profile', 'Dry-cured for extended kitchen storage', 'Uniform grading (50-60mm)'],
    nutrition: { calories: '40 kcal', carbs: '9.3g', quercetin: 'High', vitaminB6: '8% RDA' },
    shelfLife: '3-4 weeks dry ventilated'
  },
  {
    id: 'prod-basmati-rice',
    slug: 'traditional-taraori-basmati-rice',
    name: 'Traditional Aged Taraori Basmati Rice',
    categorySlug: 'grains-pulses',
    categoryName: 'Grains & Pulses',
    price: 145,
    farmerPrice: 115,
    marketPrice: 195,
    unit: '1 kg pack',
    image: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80',
    fpoName: 'Karnal Organic Rice Growers Union',
    fpoLocation: 'Karnal, Haryana',
    farmerLead: 'Harpreet Singh',
    freshnessTag: '2-Year Aged Batch',
    rating: 4.9,
    ratingCount: 220,
    inStock: true,
    stockKg: 600,
    organicCertified: true,
    description: 'Aromatic extra-long grain authentic Basmati rice naturally aged for 24 months in wooden granaries for fluffy, non-sticky cooking.',
    highlights: ['24-month natural aged grain', 'Kernel elongates up to 2.2x when cooked', 'Exquisite natural nutty Basmati aroma'],
    nutrition: { calories: '350 kcal', carbs: '78g', protein: '7.5g', fat: '0.6g' },
    shelfLife: '24 months dry container'
  },
  {
    id: 'prod-unpolished-toor-dal',
    slug: 'unpolished-desi-toor-dal',
    name: 'Desi Unpolished Toor Dal (Arhar Dal)',
    categorySlug: 'grains-pulses',
    categoryName: 'Grains & Pulses',
    price: 155,
    farmerPrice: 125,
    marketPrice: 198,
    unit: '1 kg pack',
    image: 'https://images.unsplash.com/photo-1585996656795-36423c4a2a11?auto=format&fit=crop&w=800&q=80',
    fpoName: 'Latur Pulses Producer Company',
    fpoLocation: 'Latur, Marathwada, Maharashtra',
    farmerLead: 'Balaji Kulkarni',
    freshnessTag: 'Cold Pressed & Unpolished',
    rating: 4.85,
    ratingCount: 140,
    inStock: true,
    stockKg: 400,
    organicCertified: true,
    description: 'Native Marathwada Toor Dal milled with traditional stone chakki without water polishing, chemical oils, or synthetic coloring agents.',
    highlights: ['Zero oil or leather polishing', 'Retains natural wholesome nutrient layer', 'Rich taste and authentic earthy aroma'],
    nutrition: { calories: '343 kcal', protein: '22.3g', dietaryFiber: '15g', iron: '5.1mg' },
    shelfLife: '12 months dry storage'
  },
  {
    id: 'prod-wild-forest-honey',
    slug: 'raw-wild-forest-honey',
    name: 'Raw Unprocessed Wild Forest Honey',
    categorySlug: 'organic-specials',
    categoryName: 'Organic Essentials',
    price: 320,
    farmerPrice: 250,
    marketPrice: 450,
    unit: '500 g jar',
    image: 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?auto=format&fit=crop&w=800&q=80',
    fpoName: 'Nilgiri Tribal Honey Gatherers FPO',
    fpoLocation: 'Nilgiri Biosphere, Tamil Nadu',
    farmerLead: 'Marimuthu K.',
    freshnessTag: 'Single Sourced Wild Harvest',
    rating: 4.95,
    ratingCount: 190,
    inStock: true,
    stockKg: 150,
    organicCertified: true,
    description: 'Unfiltered, unpasteurized wild multi-flora honey harvested sustainably by tribal gatherers from high forest cliffs.',
    highlights: ['Never micro-filtered or heat-treated', 'Natural pollens and enzymes intact', 'Zero added sugar or jaggery syrups'],
    nutrition: { calories: '304 kcal', sugars: '82g', enzymes: 'Active diastase', antioxidants: 'High' },
    shelfLife: 'Indefinite raw honey stability'
  },
  {
    id: 'prod-organic-turmeric',
    slug: 'lakadong-high-curcumin-turmeric',
    name: 'Lakadong High-Curcumin Turmeric Powder',
    categorySlug: 'organic-specials',
    categoryName: 'Organic Essentials',
    price: 180,
    farmerPrice: 140,
    marketPrice: 260,
    unit: '250 g pack',
    image: 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=800&q=80',
    fpoName: 'Jaintia Hills Organic Spices FPC',
    fpoLocation: 'Lakadong, Meghalaya',
    farmerLead: 'Trinity Saioo',
    freshnessTag: '7.8% Curcumin Lab Verified',
    rating: 4.9,
    ratingCount: 165,
    inStock: true,
    stockKg: 200,
    organicCertified: true,
    description: 'World-famous Lakadong turmeric containing over 7.5% natural curcumin (regular market turmeric has only 2-3%). Intensely aromatic with golden glow.',
    highlights: ['Curcumin > 7.5% verified', 'Shade dried and stone ground cold', 'Unmatched anti-inflammatory potency'],
    nutrition: { curcumin: '7.82%', essentialOils: '5.2%', purity: '100% Rhizome' },
    shelfLife: '18 months sealed pack'
  },
  {
    id: 'prod-cauliflower-snowball',
    slug: 'fresh-snowball-cauliflower',
    name: 'Snowball Fresh Cauliflower (Gobhi)',
    categorySlug: 'vegetables',
    categoryName: 'Vegetables',
    price: 38,
    farmerPrice: 30,
    marketPrice: 52,
    unit: '1 pc (~750g)',
    image: 'https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?auto=format&fit=crop&w=800&q=80',
    fpoName: 'Sonipat Vegetable Growers Society',
    fpoLocation: 'Sonipat, Haryana',
    farmerLead: 'Joginder Singh',
    freshnessTag: 'Harvested Today 4:30 AM',
    rating: 4.75,
    ratingCount: 95,
    inStock: true,
    stockKg: 300,
    organicCertified: false,
    description: 'Milky-white compact heads shielded naturally by protective green jackets. Tender florets with sweet earthy taste.',
    highlights: ['Protected curd harvest', 'Crisp florets, zero insect damage', 'Rich source of choline and vitamin C'],
    nutrition: { calories: '25 kcal', dietaryFiber: '2g', vitaminC: '77% RDA', folate: '14% RDA' },
    shelfLife: '5-7 days refrigerated'
  },
  {
    id: 'prod-nagpur-oranges',
    slug: 'nagpur-mandarin-sweet-oranges',
    name: 'Nagpur Sweet Mandarin Oranges (Santra)',
    categorySlug: 'fruits',
    categoryName: 'Fresh Fruits',
    price: 85,
    farmerPrice: 65,
    marketPrice: 120,
    unit: '1 kg (5-6 pcs)',
    image: 'https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?auto=format&fit=crop&w=800&q=80',
    fpoName: 'Vidarbha Citrus Producers FPO',
    fpoLocation: 'Nagpur, Maharashtra',
    farmerLead: 'Prakash Deshmukh',
    freshnessTag: 'Tree Ripened Orchard Batch',
    rating: 4.8,
    ratingCount: 130,
    inStock: true,
    stockKg: 500,
    organicCertified: false,
    description: 'Juicy, easy-to-peel authentic Nagpur mandarins packed with invigorating citrus juice and vibrant natural vitamin C.',
    highlights: ['Naturally tree ripened', 'Thin skin with luscious juice sacs', 'High juice yield per fruit'],
    nutrition: { calories: '47 kcal', vitaminC: '89% RDA', potassium: '181mg', sugars: '9.4g' },
    shelfLife: '8-12 days cool dry'
  }
];

export const getProductById = (id) => PRODUCTS.find((p) => p.id === id || p.slug === id);

export const getProductsByCategory = (categorySlug) => {
  if (!categorySlug || categorySlug === 'all') return PRODUCTS;
  return PRODUCTS.filter((p) => p.categorySlug === categorySlug);
};

// Intelligent Fuzzy Search Configuration via Fuse.js
const FUSE_SEARCH_OPTIONS = {
  threshold: 0.4,
  ignoreLocation: true,
  minMatchCharLength: 2,
  includeScore: true,
  shouldSort: true,
  keys: [
    { name: 'name', weight: 0.7 },
    { name: 'categoryName', weight: 0.4 },
    { name: 'fpoName', weight: 0.3 },
    { name: 'fpoLocation', weight: 0.3 },
    { name: 'description', weight: 0.3 },
    { name: 'highlights', weight: 0.2 },
    { name: 'farmerLead', weight: 0.2 }
  ]
};

const fuseInstance = new Fuse(PRODUCTS, FUSE_SEARCH_OPTIONS);

export const searchProducts = (query, categorySlug = 'all') => {
  const pool = getProductsByCategory(categorySlug);
  if (!query || !query.trim()) return pool;

  const q = query.trim();

  // For single-character queries, provide crisp exact substring matches
  if (q.length === 1) {
    const char = q.toLowerCase();
    return pool.filter(
      (p) =>
        p.name.toLowerCase().includes(char) ||
        p.categoryName.toLowerCase().includes(char) ||
        p.description.toLowerCase().includes(char)
    );
  }

  // Multi-character fuzzy search with Fuse.js (handles typos like 'tomoto', 'tomtao' and partials like 'tom', 'app')
  const results = fuseInstance.search(q);

  // Filter out distant noise (score > 0.84) while preserving fuzzy matches and typos
  let matchedProducts = results
    .filter((r) => r.score <= 0.84)
    .map((r) => r.item);

  // If score filtering pruned all results but a top match exists with reasonable score, retain it
  if (matchedProducts.length === 0 && results.length > 0 && results[0].score <= 0.88) {
    matchedProducts = [results[0].item];
  }

  // Filter by category if specified
  if (categorySlug && categorySlug !== 'all') {
    matchedProducts = matchedProducts.filter((p) => p.categorySlug === categorySlug);
  }

  return matchedProducts;
};
